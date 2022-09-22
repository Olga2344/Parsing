import scrapy
from scrapy.http import HtmlResponse
from pars_stroy_market.items import ParsStroyMarketItem
from scrapy.loader import ItemLoader


class CastoramaRuSpider(scrapy.Spider):
    name = 'castorama_ru'
    allowed_domains = ['castorama.ru']
    

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://www.castorama.ru/gardening-and-outdoor/pochtovye-jaschiki"]

    def parse(self, response:HtmlResponse):
        pages_links = response.xpath("//a[contains(@class, 'product-card__name')]")
        for link in pages_links:
            yield response.follow(link, callback=self.parse_goods)    

    def parse_goods(self, response:HtmlResponse):
        
        #print('\n\###########\n%s\n\########\n' %response.url)

        loader = ItemLoader(item=ParsStroyMarketItem(), response=response)
        
        loader.add_xpath('name', "//a[contains(@class,'product-card__name')]/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[contains(@class,'price')]//child::*/text()")
        loader.add_xpath('photos', "//img[contains=@class, 'product-card__img']//@data_src")
        yield loader.load_item()
        

