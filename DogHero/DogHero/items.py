# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def street_process (value):
    value = value.split("-")
    return value[0].strip()
    
def feature_process (value):
    value = remove_tags(value)
    value = value.replace('.','')
    return value.strip().split()[0]

def price_extra_process (value):
    return value.replace(u"\xa0", u' ')

class ImovelItem (scrapy.Item):
    title = scrapy.Field(
        input_processor= MapCompose(str.strip)
    )

    filter_purchase = scrapy.Field(
        input_processor= MapCompose(street_process)
    )

    filter_type = scrapy.Field(
        input_processor= MapCompose(street_process)
    )

    location_street = scrapy.Field( 
        input_processor= MapCompose(street_process)
    )
    
    location_neigh_city = scrapy.Field(
        input_processor= MapCompose(remove_tags ,str.strip)
    )

    features_area = scrapy.Field(
        input_processor= MapCompose(feature_process)
    )

    features_bedrooms = scrapy.Field(
        input_processor= MapCompose(feature_process)
    )

    features_bathrooms = scrapy.Field(
        input_processor= MapCompose(feature_process)
    )

    price_original = scrapy.Field( 
        input_processor= MapCompose(str.strip)
    )
    price_extra = scrapy.Field( 
        input_processor= MapCompose(str.strip, price_extra_process)
    )


def price_process (value):
    value = value.replace('.','')
    value = value.replace(',','.')
    return value.split(' ')[1]

def neighbor_process (value):
    return value.split(',')[1].strip()
    
def city_process (value):
    return value.split(',')[2].strip()

def area_process (value):
    return value.replace('m2','')

def saletype_process(value):
    return value.split(' ', 1)

class ImovelItemLoader(ItemLoader):
    default_item_class = ImovelItem
    default_output_processor = TakeFirst()

class CrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Venda = scrapy.Field( 
        input_processor = MapCompose(price_process),
        output_processor= TakeFirst()
    )
    Aluguel = scrapy.Field( 
        input_processor = MapCompose(price_process),
        output_processor= TakeFirst()
    )
    Condomínio = scrapy.Field( 
        input_processor = MapCompose(price_process),
        output_processor= TakeFirst()
    )
    IPTU = scrapy.Field( 
        input_processor = MapCompose(price_process),
        output_processor= TakeFirst()
    )

    saletype = scrapy.Field( 
        output_processor= TakeFirst()
    )
    street = scrapy.Field( 
        output_processor= TakeFirst()
    )
    neigghborhood_city = scrapy.Field( 
        output_processor= TakeFirst()
    )
    title = scrapy.Field( 
        output_processor= TakeFirst()
    )

    features = scrapy.Field()
    featurestype = scrapy.Field()

    # privateareas = scrapy.Field()
    # commonareas = scrapy.Field()
    # diverseareas = scrapy.Field()

class CrawlItemLoader(ItemLoader):
    default_item_class = CrawlItem
    default_input_processor = MapCompose(str.strip)

class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Venda = scrapy.Field( 
        input_processor = MapCompose(price_process)
    )
    Aluguel = scrapy.Field( 
        input_processor = MapCompose(price_process)
    )
    Condominio = scrapy.Field( 
        input_processor = MapCompose(price_process)
    )
    IPTU = scrapy.Field( 
        input_processor = MapCompose(price_process)
    )

    saletype = scrapy.Field(
        input_processor = MapCompose(saletype_process)
    )
    street = scrapy.Field()
    neigghborhood = scrapy.Field( 
        input_processor = MapCompose(neighbor_process)
    )
    city = scrapy.Field( 
        input_processor = MapCompose(city_process)
    )
    title = scrapy.Field( )

    area_total = scrapy.Field( 
        input_processor = MapCompose(area_process)
    )
    area_util = scrapy.Field( 
        input_processor = MapCompose(area_process)
    )

    banheiro = scrapy.Field( )
    vaga = scrapy.Field( )
    quarto = scrapy.Field( )
    suite = scrapy.Field( )
    age_imovel = scrapy.Field( )

    privateareas = scrapy.Field()
    commonareas = scrapy.Field()
    diverseareas = scrapy.Field()

class CrawlerItemLoader(ItemLoader):
    default_item_class = CrawlerItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()