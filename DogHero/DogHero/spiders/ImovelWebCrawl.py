# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from DogHero.items import CrawlItem, CrawlItemLoader
from scrapy.selector import Selector    

totalpages = 5

class ImovelwebcrawlSpider(CrawlSpider):
    name = 'ImovelWebCrawl'
    allowed_domains = ['www.imovelweb.com.br']
    start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-pagina-_%s.html' % page for page in range(1,totalpages+1)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths= "//li[contains(@class, 'aviso aviso-desktop')]"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths= "//li[@class = 'pagination-action-next ']/a"), callback='parse_item', follow=True)
    )

    custom_settings = {
        'FEED_FORMAT':"csv",
        'FEED_URI':"imovelcrawl.csv"
    }

    def parse_item(self, response):
        loader = CrawlItemLoader(selector=Selector(response), response= response)
        loader.add_xpath('Venda', "//div[@class='price-operation' and text() = 'Venda']/following-sibling::node()/span/text()")
        loader.add_xpath('Aluguel', "//div[@class='price-operation' and text() = 'Aluguel']/following-sibling::node()/span/text()")
        loader.add_xpath('Condomínio', "//div[@class='block-expensas block-row' and text() = 'Condomínio ']/span/text()")
        loader.add_xpath('IPTU', "//div[@class='block-expensas block-row' and text() = 'IPTU ']/span/text()")

        loader.add_xpath('saletype', "//h2[@class='title-type-sup']/b/text()")
        loader.add_xpath('street', "//h2[@class='title-location']/b/text()")
        loader.add_xpath('neigghborhood_city', "//h2[@class='title-location']/span/text()")
        loader.add_xpath('title', "//div[@class='section-title']/h1/text()")

        # here we run first to figure out every type of feature there is
        # then we scrap every feature separately in the final version
        loader.add_xpath('features', "//li[@class='icon-feature']/b/text()")
        loader.add_xpath('featurestype', "//li[@class='icon-feature']/span/text()")

        # loader.add_xpath('privateareas', "//div[h4[text()='Áreas Privativas']]/following-sibling::node()[2]/li/h4/text()")
        # loader.add_xpath('commonareas', "//div[h4[text()='Áreas Comuns']]/following-sibling::node()[2]/li/h4/text()")
        # loader.add_xpath('diverseareas', "//div[h4[text()='Outros']]/following-sibling::node()[2]/li//text()")
        
        yield loader.load_item()