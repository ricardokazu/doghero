# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from DogHero.items import CrawlerItem, CrawlerItemLoader
from scrapy.selector import Selector    

totalpages = 2000

class ImovelwebcrawlSpider(CrawlSpider):
    name = 'ImovelWebCrawl_final'
    allowed_domains = ['www.imovelweb.com.br']
    start_urls = ['https://www.imovelweb.com.br/imoveis-pagina-%s.html' % page for page in range(1,totalpages+1)]
    # start_urls = ['https://www.imovelweb.com.br/imoveis.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths= "//li[contains(@class, 'aviso aviso-desktop')]"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths= "//li[@class = 'pagination-action-next ']/a"), callback='parse_item', follow=True)
    )

    custom_settings = {
        'FEED_FORMAT':"csv",
        'FEED_URI':"imovelwebcrawl.csv"
    }

    def parse_item(self, response):
        loader = CrawlerItemLoader(selector=Selector(response), response= response)
        loader.add_xpath('Venda', "//div[@class='price-operation' and text() = 'Venda']/following-sibling::node()/span/text()")
        loader.add_xpath('Aluguel', "//div[@class='price-operation' and text() = 'Aluguel']/following-sibling::node()/span/text()")
        loader.add_xpath('Condominio', "//div[@class='block-expensas block-row' and text() = 'Condomínio ']/span/text()")
        loader.add_xpath('IPTU', "//div[@class='block-expensas block-row' and text() = 'IPTU ']/span/text()")

        loader.add_xpath('saletype', "//h2[@class='title-type-sup']/b/text()")
        loader.add_xpath('street', "//h2[@class='title-location']/b/text()")
        loader.add_xpath('neigghborhood', "//h2[@class='title-location']/span/text()")
        loader.add_xpath('city', "//h2[@class='title-location']/span/text()")
        loader.add_xpath('title', "//div[@class='section-title']/h1/text()")

        # we scrap every feature separately
        loader.add_xpath('area_total', "//li[@class='icon-feature']/span[contains(text(),'Área total')]/preceding-sibling::node()/text()")
        loader.add_xpath('area_util', "//li[@class='icon-feature']/span[contains(text(),'Área útil')]/preceding-sibling::node()/text()")
        loader.add_xpath('banheiro', "//li[@class='icon-feature']/span[contains(text(),'Banheiro')]/preceding-sibling::node()/text()")
        loader.add_xpath('vaga', "//li[@class='icon-feature']/span[contains(text(),'Vaga')]/preceding-sibling::node()/text()")
        loader.add_xpath('quarto', "//li[@class='icon-feature']/span[contains(text(),'Quarto')]/preceding-sibling::node()/text()")
        loader.add_xpath('suite', "//li[@class='icon-feature']/span[contains(text(),'Suíte')]/preceding-sibling::node()/text()")
        loader.add_xpath('age_imovel', "//li[@class='icon-feature']/span[contains(text(),'Idade')]/preceding-sibling::node()/text()")

        loader.add_xpath('privateareas', "//div[h4[text()='Áreas Privativas']]/following-sibling::node()[2]/li/h4/text()")
        loader.add_xpath('commonareas', "//div[h4[text()='Áreas Comuns']]/following-sibling::node()[2]/li/h4/text()")
        loader.add_xpath('diverseareas', "//div[h4[text()='Outros']]/following-sibling::node()[2]/li//text()")
        
        yield loader.load_item()