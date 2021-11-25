import re
import pandas as pd
from datetime import date

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WildbressSpider(CrawlSpider):
    name = "wildbress"
    allowed_domains = ["www.wildberries.ru"]
    start_urls = ["https://www.wildberries.ru/catalog/pitanie"]
    rules = (
        Rule(LinkExtractor(allow=([r'/catalog/pitanie/', r'/catalog/produkty/']))),
        Rule(LinkExtractor(allow=(r'/detail.aspx',)), callback='parse_item'),
    )
    shop_id = 5
    file_name = f'{name}_{date.today()}.csv'

    def get_dict(self, table: pd.DataFrame) -> dict:
        data = {}
        headers = table[0]
        values = table[1]
        index = -1
        for header in headers:
            index += 1
            data.update({header: values[index]})
        return data

    def parse_item(self, response):
        self.logger.info(f'Сейчас на этой ссылке {response.url}')
        sale_price_check = response.xpath('//del[@class="price-block__old-price j-final-saving"]').get()
        if sale_price_check:
            old_price = re.sub(
                '[^0-9]',
                '',
                response.xpath('//del[@class="price-block__old-price j-final-saving"]/text()').get()
            )
        name = ' '.join(response.xpath('//h1[@class="same-part-kt__header"]/span/text()').getall())
        description = response.xpath('//div[@class="collapsable__content j-description"]/p/text()').get()
        sostav = response.xpath('//div[@class="collapsable__content j-consist"]/p/text()').get()
        table = pd.read_html(response.xpath('//table[@class="product-params__table"]').get())
        data = self.get_dict(table[0])
        price = re.sub(
            '[^0-9]',
            '',
            response.xpath('//span[@class="price-block__final-price"]/text()').get()
        )
        article = re.sub(
            '[^0-9]',
            '',
            response.xpath('//span[@data-link="text{: selectedNomenclature^cod1S}"]/text()').get()
        )

        product = {
            'article': article,
            'sale_price': price if sale_price_check else None,
            'price': old_price if sale_price_check else price,
            'name': name,
            'url': response.url,
            'description': description if description else None,
            'sostav': sostav if sostav else None
        }
        product.update(data)
        yield product

    def close(self, reason):
        from core.crud.porduct import CRUDProduct
        from core.db.database import Session, engine

        crud = CRUDProduct()
        crud.add_product_by_file(session=Session(engine), file_name=self.file_name, shop_id=self.shop_id)
        #TODO dobavit otpravku faila po zaversheniu parsinga

