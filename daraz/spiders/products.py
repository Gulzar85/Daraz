import scrapy
import json
from time import sleep
from random import randint
from datetime import date
import scraper_helper as sh

class ProductsSpider(scrapy.Spider):
    name = 'products'
    ransom_user_agent = True
    def start_requests(self):
        for page in range(1,10):
            sleep(randint(8,15))
            url = 'https://www.daraz.pk/kitchen-dining/?page={}&spm=a2a0e.home.cate_7.5.35e34937ytg2Tw'.format(page)
            yield scrapy.Request(url)


    def parse(self, response):
        Processed_SKU = set()
        for script in response.css('script::text').getall():
            if 'window.pageData=' in script:
                data = json.loads(script.split('window.pageData=')[-1])
                json_data = data['mods']['listItems']
                for phone in json_data:
                    SKU = phone['sku']
                    if SKU not in Processed_SKU:
                        Processed_SKU.add(phone['sku'])
                        yield {
                            'Date': date.today(),
                            'Name': sh.cleanup(phone['name']),
                            'Brand Name': phone['brandName'],
                            'Avilability': bool(phone['inStock']),
                            'Price': float(phone['price']),
                            'Rating Score': float(phone['ratingScore']),
                            'Reviews': int(phone['review']),
                            'Seller Name': phone['sellerName'],
                            'SKU': phone['sku'],
                            'Product URL': phone['productUrl'],
                            'Image URL': phone['image'],
                            'Location': phone['location'],
                            'Page_URL': response.url,
                        }