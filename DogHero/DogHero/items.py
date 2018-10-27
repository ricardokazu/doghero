# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

class DogheropsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def street_process (value):
    value = value.split("-")
    return value[0].strip()

class PriceMeta (scrapy.Item):
    price_original = scrapy.Field( 
        input_processor= MapCompose(str.strip),
        output_processor= TakeFirst()
    )
    price_extra = scrapy.Field( 
        input_processor= MapCompose(str.strip),
        output_processor= TakeFirst()
    )

class ImovelItem (scrapy.Item):
    title = scrapy.Field(
        input_processor= MapCompose(str.strip),
        output_processor= TakeFirst()
    )

    location_street = scrapy.Field( 
        input_processor= MapCompose(street_process),
        output_processor= TakeFirst()
    )
    
    location_city = scrapy.Field(
        input_processor= MapCompose(remove_tags ,str.strip),
        output_processor= TakeFirst()
    )

    features = scrapy.Field(
        input_processor= MapCompose(remove_tags, str.strip),
        output_processor= Join(' ')
    )

    price = scrapy.Field(serializer = PriceMeta)

class MainItemLoader(ItemLoader):
    default_item_class = ImovelItem
    default_output_processor = TakeFirst()

class PriceItemLoader(ItemLoader):
    default_item_class = PriceMeta
    default_output_processor = TakeFirst()