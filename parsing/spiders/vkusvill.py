import re
import unicodedata
from datetime import date

from scrapy.spiders import SitemapSpider


class VkusvillSpider(SitemapSpider):
    name = "vkusvill"
    sitemap_urls = ['https://vkusvill.ru/upload/sitemap/msk/sitemap_goods.xml',]
    file_name = f'{name}_{date.today()}.csv'
    shop_id = 4

    def parse(self, response, **kwargs):
        if response.xpath('//img[@class="lazyload"]/@title').get() is not None:
            name = response.xpath('//img[@class="lazyload"]/@title').get()
            image_url = response.xpath('//img[@class="lazyload"]/@data-src').get()
            price = response.xpath('//meta[@itemprop=\"price\"]/@content').get()
            ves_and_year = response.xpath('//li[@class="Product__listItem"]/text()').getall()
            try:
                ed_izm = response.xpath('//span[@class="Price__unit"]/text()').getall()[1]
                ves = re.sub("[^0-9]", "", ves_and_year[1])
            except IndexError:
                print('0 значение')
            category_list = response.xpath('//span[@class="Breadcrumbs__link"]/a/@title').getall()
            id = response.xpath('//div[@class="Product__col Product__col--content js-product-cart js-datalayer-detail'
                                ' js-datalayer-catalog-list-item"]/@data-xmlid').get()
            product = {
                'name': name,
                'unit': ed_izm.replace(' ', '').replace('/', '').replace('\xa0\xa0', ''),
                'price': price,
                'weight': ves,
                'image_url': image_url,
                'url': response.url,
                'category': category_list,
                'article': id,
            }
            yield product
        else:
            pass

    def close(self, reason):
        from core.crud.porduct import CRUDProduct
        from core.db.database import Session, engine

        crud = CRUDProduct()
        crud.add_product_by_file(session=Session(engine), file_name=self.file_name, shop_id=self.shop_id)
        #TODO dobavit otpravku faila po zaversheniu parsinga




