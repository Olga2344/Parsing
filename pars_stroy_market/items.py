# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from multiprocessing.sharedctypes import Value
import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def clean_price(value):
    value=int((value[0]).replace(' ', ''))
    return value

def clean_name(val):
    try:
        val = val.strip()
    except:
        return val
    return val

class ParsStroyMarketItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(clean_name),output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
    
