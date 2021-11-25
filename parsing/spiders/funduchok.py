import re
from datetime import date

from scrapy.spiders import SitemapSpider


class FunduchokSpider(SitemapSpider):
    name = "funduchok"
    sitemap_urls = ['https://xn--d1amhfwcd2a.xn--p1ai/sitemap.xml',]
    file_name = f'{name}_{date.today()}.csv'
    shop_id = 1

    def get_price_to_kg(self, price_block):
        block = price_block.xpath('//label[@class="label label--packaging-card"]')
        for price_element in block:
            ves_element = price_element
            ves = ves_element.xpath('//span[@class="color--weight"]/text()').get()
            ves = re.sub('[^0-9]', '', ves)
            if ves == '1':
                price = price_element.xpath('//span[@class="old-price"]/text()').get()
                price = re.sub('[^0-9]', '', price)
                return {'ves': ves, 'price': price}
            else:
                continue

    def parse(self, response, **kwargs):
        price = response.xpath('//meta[@itemprop="price"]/@content').get()
        if price:
            prod_name = response.xpath('//h1[@class="h1 text-align-left"]/text()').get()
            image_url = response.xpath('//a[@class="product__card__gallery__element__image-link"]/@src').get()
            product_id = response.xpath('//input[@type="hidden"]/@value').get()
            category_list = response.xpath('//ul[@class="breadcrumb__list"]/li/a/span/text()').getall()
            category = '|'.join(category_list)
            discount = response.xpath('//span[@class="discount__value color--price-card"]/text()').get()
            if discount:
                discount = re.sub('[^0-9]', '', discount)
                sale_price = int(price) - (int(price) / 100 * int(discount))
            product = {
                'name': prod_name,
                'image_url': 'https://xn--d1amhfwcd2a.xn--p1ai' + image_url if image_url else None,
                'category': category,
                'url': response.url,
                'article': product_id,
                'price': price,
                'sale_price': sale_price if discount else None,
                'unit': 'кг',
                'weight': '1'
            }
            yield product
        else:
            pass

    def close(self, reason):
        from core.crud.porduct import CRUDProduct
        from core.db.database import session

        crud = CRUDProduct()
        crud.add_product_by_file(session=session, file_name=self.file_name, shop_id=self.shop_id)
        #TODO dobavit otpravku faila po zaversheniu parsinga













