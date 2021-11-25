from decimal import Decimal
import re

from requests import request
from bs4 import BeautifulSoup


rf_url = "https://api.rf.market/api/integration/products?page=1"
rf_url_format = "https://api.rf.market/api/integration/products/{prod_id}"


class PriceShopParser:

    def parser(self, url):
        methods = {
            'фундучок.рф': self.price_funduchok,
            'ecomarket.ru': self.price_ecomarket,
            'www.utkonos.ru': self.price_utkonos,
            'vkusvill.ru': self.price_vkusvill,
            'www.wildberries.ru': self.price_wildberries,
            'www.delikateska.ru': self.price_delicateska,
            'ryboedov.ru': self.price_ryboedov,

        }
        key = re.search('https?://([А-Яа-яA-Za-z_0-9.-]+).*', url)
        if key:
            return methods[key.group(1)]

    def price_rf(self, prod_id):
        rs = request(url=rf_url_format.format(prod_id=prod_id), method='GET')
        price = rs.json()['data']['price']
        return price

    def price_ecomarket(self, url: str):
        api = 'https://api.ecomarket.ru/api.php'
        format_url = url.replace('https://ecomarket.ru/', '')
        json = {
            "action": "getProductByUrl_v2",
            "url": format_url,
            "region": "77",
            "token": "c1d386c2416e54d5abd6cd5c01d26f59"
        }
        rs = request('POST', api, json=json)
        response = rs.json()
        data = dict(
            price=response['data']['old_price'] if response['data']['old_price'] else response['data']['price'],
            name=response['data']['title'],
            article=response['data']['id'],
            url='https://api.ecomarket.ru/' + response['data']['url'],
            shop='экомаркет',
            sale_price=response['data']['price'] if response['data']['old_price'] else None
        )
        return data

    def price_utkonos(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        if soup.find('span', class_='product-sale-price title-l1 __accent ng-star-inserted'):
            data = dict(
                price=re.sub(
                    '[^0-9,]',
                    '',
                    soup.find('span', class_='product-sale-price title-l1 __accent ng-star-inserted').text
                ).replace(',', '.'),
                name=soup.find('h1', class_='product-base-info_name title-l2 ng-star-inserted').get('itemprop'),
                article=re.sub('[^0-9]', '', soup.find('span', class_='product-base-info_vendor-code').text),
                url=url,
                shop='утконос',
            )
        else:
            data = dict(
                price=re.sub(
                    '[^0-9,]',
                    '',
                    soup.find('span', class_='product-sale-price title-l1 ng-star-inserted').text
                ).replace(',', '.'),
                name=soup.find('h1', class_='product-base-info_name title-l2 ng-star-inserted').get('itemprop'),
                article=re.sub('[^0-9]', '', soup.find('span', class_='product-base-info_vendor-code').text),
                url=url,
                shop='утконос',
            )
        return data

    def price_funduchok(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        if soup.find('input', class_='input input--radio'):
            price = soup.find_all('label', class_='label label--packaging-card')[-1]
            data = dict(
                price=price.find('input', class_='input input--radio').get('data-price'),
                name=soup.find('h1', class_='h1 text-align-left').text,
                article=soup.find('input', {'type': 'hidden'}).get('value'),
                url=url,
                shop='фундучок'
            )
        else:
            price = soup.find('span', class_='product__card__options__action__value color--price-card').text
            data = dict(
                price=re.sub('[^0-9,]', '', price).replace(',', '.'),
                name=soup.find('h1', class_='h1 text-align-left').text,
                article=soup.find('input', {'type': 'hidden'}).get('value'),
                url=url,
                shop='фундучок'
            )

        return data

    def price_wildberries(self, url: str):
        rs = request(method='GET', url=url)
        soup = BeautifulSoup(rs.text, "lxml")
        data = dict(
                name=soup.find('h1', class_='same-part-kt__header').text,
                article=re.sub('[^0-9]', '', soup.find('p', class_='same-part-kt__article').text),
                url=url,
                shop='wildberries'
            )
        if soup.find('del', class_='price-block__old-price j-final-saving'):
            data.update(dict(
                sale_price=re.sub('[^0-9]', '', soup.find('span', class_='price-block__final-price').text),
                price=re.sub('[^0-9]', '', soup.find('del', class_='price-block__old-price j-final-saving').text),
            ))
            return data
        else:
            data.update(dict(
                price=re.sub('[^0-9]', '', soup.find('span', class_='price-block__final-price').text),
            ))
            return data

    def price_vkusvill(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        data = dict(
            price=soup.find('span', class_='Price__value').text,
            name=soup.find('h1', class_='Product__title js-datalayer-catalog-list-name').text,
            article=soup.find(
                'div',
                class_='Product__col Product__col--content js-product-cart '
                       'js-datalayer-detail js-datalayer-catalog-list-item').get('data-xmlid'),
            url=url,
            shop='вкусвилл'
        )

        return data

    def price_delicateska(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, 'lxml')
        data = dict(
            name=soup.find('h1', class_='title').text,
            price=soup.find('div', itemprop='price').get('content'),
            article=re.sub('[^0-9]', '', soup.find('span', class_='article').text),
            url=url,
            shop='Деликатеска'

        )
        return data

    def price_ryboedov(self, url: str):
        rs = request(method='GET', url=url)
        soup = BeautifulSoup(rs.text, 'lxml')
        data = dict(
            name=soup.find('h1').text,
            price=re.sub('[^0-9]', '', soup.find('div', class_='catalog-price').find('strong').text),
            article=re.sub('[^0-9]', '', soup.find('div', class_='articul2').text),
            url=url,
            shop='Рыбоедов'
        )
        return data

    def compare(self, url, product_id=None):

        if product_id:
            rf_price = self.price_rf(product_id)
            shop = self.parser(url)
            data = shop(url)
            shop_price = shop(url)['price']
            different_price = Decimal(shop_price) - Decimal(rf_price)
            data.update({'different_price': different_price})
            return data
        else:
            shop = self.parser(url)
            data = shop(url)
            return data

