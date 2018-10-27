import scrapy
from scrapy.loader import ItemLoader
from DogHero.items import ImovelItem, MainItemLoader, PriceItemLoader
from scrapy.selector import Selector    

class ImovelWebSpider (scrapy.Spider):
    # identify
    name = "imovelweb"

    # Request
    start_urls = ['https://www.imovelweb.com.br/apartamentos-padrao-venda.html']
    custom_settings = {
        'FEED_FORMAT':"csv",
        'FEED_URI':"imovelweb.csv"
    }

    #Response
    def parse(self,response):
        for imovel in response.xpath("//li[contains(@class, 'aviso aviso-desktop')]"):
            loader = MainItemLoader(Item = imovel, selector=Selector(response), response= response)
            loader.add_xpath('title', ".//h4[@class='aviso-data-title']/a/text()")
            loader.add_xpath('location_street', ".//span[contains(@class, 'aviso-data-location')]/text()[1]")
            loader.add_xpath('location_city', ".//span[contains(@class, 'aviso-data-location')]/span")
            #loader.add_xpath('features', ".//ul[@class = 'aviso-data-features dl-aviso-link']/text()")
            loader.add_xpath('features', ".//ul[contains(@class, 'aviso-data-features')]/li/child::node()[position()=1 or position()= 2]")
            loader.add_value('price', self.get_price(imovel, response))
            yield loader.load_item()

        # /quotes?page=2
#        next_page= response.xpath("//li[contains(@class,'pagination-action-next')]/a/@href").extract_first()
#        if next_page is not None:
#            next_page_link= response.urljoin(next_page)
#            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def get_price(self, Item,  response):
        loader = PriceItemLoader(Item = Item, selector=Selector(response), response= response)
        loader.add_xpath('price_original', ".//div[@class='aviso-data-price-content']/span[contains(@class, 'aviso-data-price-value')]/text()")
        loader.add_xpath('price_extra', ".//div[@class='aviso-data-price-content']/span[contains(@class, 'aviso-data-expensas-value')]/text()")