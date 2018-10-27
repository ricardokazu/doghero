# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

class DogheropsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def street_process (value):
    value = value.split("-")
    return value[0].strip()

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

    price = scrapy.Field(
        input_processor= MapCompose(str.strip),
        output_processor= TakeFirst()
    )

    price_condo = scrapy.Field( 
        input_processor= MapCompose(str.strip),
        output_processor= TakeFirst()
    )
