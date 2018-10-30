import scrapy
from scrapy.loader import ItemLoader
from DogHero.items import ImovelItem, ImovelItemLoader
from scrapy.selector import Selector    

totalpages = 5

class ImovelWebSpider (scrapy.Spider):
    # identify
    name = "imovelweb"

    # Request
    start_urls = ['https://www.imovelweb.com.br/apartamentos-venda.html',
        'https://www.imovelweb.com.br/casas-venda.html',
        'https://www.imovelweb.com.br/apartamentos-aluguel.html',
        'https://www.imovelweb.com.br/casas-aluguel.html']

    custom_settings = {
        'FEED_FORMAT':"csv",
        'FEED_URI':"imovelweb.csv"
    }
    
    #Response
    def parse(self,response):
        for imovel in response.xpath("//li[contains(@class, 'aviso aviso-desktop')]"):
            loader = ImovelItemLoader(selector=imovel, response= response)
            # loader.add_xpath('destaque', ".//span[contains(@class, 'destacado')]/text()")
            # loader.add_xpath('number_photos', ".//div[contains(@class, 'media-labels')]/span/@data-count)")
            loader.add_xpath('title', ".//h4[@class='aviso-data-title']/a/text()")
            loader.add_xpath('filter_purchase', "//div[@class = 'appliedfilters-tags']/ul/li/h2[text()='Comprar' or text()='Alugar']/text()")
            loader.add_xpath('filter_type', "//div[@class = 'appliedfilters-tags']/ul/li/h2[text()='Apartamentos' or text()='Casas']/text()")

            loader.add_xpath('location_street', ".//span[contains(@class, 'aviso-data-location')]/text()[1]")
            loader.add_xpath('location_neigh_city', ".//span[contains(@class, 'aviso-data-location')]/span")
            loader.add_xpath('features_area', ".//ul[contains(@class, 'aviso-data-features')]/li/span[contains(text(), 'Útil')]/preceding-sibling::node()") 
            loader.add_xpath('features_bedrooms', ".//ul[contains(@class, 'aviso-data-features')]/li/span[contains(text(), 'Quartos')]/preceding-sibling::node()")
            loader.add_xpath('features_bathrooms', ".//ul[contains(@class, 'aviso-data-features')]/li/span[contains(text(), 'Banheiros')]/preceding-sibling::node()")
            # loader.add_xpath('description', ".//p[contains(@class, 'description')]/text()")
            # loader.add_xpath('publication_date', ".//li[contains(@class,  'aviso-data-extra-item aviso-tags-publicacion')]/text()")
            loader.add_xpath('price_original', ".//div[@class='aviso-data-price-content']/span[contains(@class, 'aviso-data-price-value')]/text()")
            loader.add_xpath('price_extra', ".//div[@class='aviso-data-price-content']/span[contains(@class, 'aviso-data-expensas-value')]/text()")
            yield loader.load_item()

        curent_page = response.xpath("//li[@class='active']/a/text()").extract_first()
        
        if int(curent_page) < totalpages:
            # /quotes?page=2
            next_page= response.xpath("//li[contains(@class,'pagination-action-next')]/a/@href").extract_first()
            if next_page is not None:
                next_page_link= response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link, callback=self.parse)