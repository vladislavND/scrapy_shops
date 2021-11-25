import re
from datetime import date

from scrapy.spiders import SitemapSpider


class RiboedovSpider(SitemapSpider):
    name = "riboedov"
    sitemap_urls = ['https://ryboedov.ru/sitemap-iblock-1.xml',]
    file_name = f'{name}_{date.today()}.csv'
    shop_id = 6

    def get_unit_value(self, unit_value):
        if 'кор' in unit_value:
            return {"weight": 1, "unit": "кор"}
        if 'шт' in unit_value:
            return {"weight": 1, "unit": "шт"}
        if 'уп' in unit_value:
            return {"weight": 1, "unit": "уп"}
        if 'гр' in unit_value:
            unit_weight = re.sub('[^0-9]', '', unit_value)
            return {"weight": unit_weight, "unit": "гр"}
        if 'кг' in unit_value:
            return {"weight": 1, "unit": "кг"}

    def parse(self, response, **kwargs):
        article_str = response.xpath('//div[@class="articul2"]/text()').get()
        if article_str:
            name = response.xpath('//div[@class="content-area"]/h1/text()').get()
            article = re.sub('[^0-9]', '', article_str)
            price = response.xpath('//div[@class="catalog-price"]/strong/text()').get()
            unit = response.xpath('//span[@class="unit"]/text()').get()

            data = {
                "price": price,
                "name": name,
                "article": article,
                "url": response.url,
            }
            data.update(self.get_unit_value(unit))
            yield data
        else:
            pass

    def close(self, reason):
        from core.crud.porduct import CRUDProduct
        from core.db.database import session

        crud = CRUDProduct()
        crud.add_product_by_file(session=session, file_name=self.file_name, shop_id=self.shop_id)
        #TODO dobavit otpravku faila po zaversheniu parsinga













