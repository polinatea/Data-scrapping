import requests
import geojson
import scrapy

# Базовый URL получения данных
# URL ="https://www.edenred.fr/api/outlets?result_level=full&radius=5&page_size=30&location=48.856483%2C2.352414&supported_products=CTR_4C"

class GeoJsonPointItem(scrapy.Item):
    lat = scrapy.Field()
    lon = scrapy.Field()
    name = scrapy.Field()
    addr_full = scrapy.Field()
    housenumber = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    country = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    store_url = scrapy.Field()
    email = scrapy.Field()
    opening_hours = scrapy.Field()
    ref = scrapy.Field()
    brand = scrapy.Field()
    brand_wikidata = scrapy.Field()
    extras = scrapy.Field()

class Edenred_Spider(scrapy.Spider):
    start_urls = ["https://www.edenred.fr/api/outlets?result_level=full&radius=5&page_size=30&location=48.856483%2C2.352414&supported_products=CTR_4C"]
    name = 'edenred'
    allowed_domains = ['edenred.fr']

    def parse(self,response):
        data = response.json()
        # print(data)
        for row in data:
            print(row)
            item = GeoJsonPointItem()
            item["red"] = row["outlet_ref"]
            item["name"] = row["title"]
            
            item['addr_full'] = row["address"]["street_name"]
            item["city"] = row["address"]["city_name"]
            item["lat"] = float(row["address"]["latitude"])
            item["lon"] = float(row["address"]["longitude"])

            yield item
    #     print(elem["title"],"______________",elem["address"]["city_name"])