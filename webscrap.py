import scrapy


class DmartSpider(scrapy.Spider):
    name = 'vegetables'
    allowed_domains = ['www.dmart.in/vegetables']
    start_urls = ['http://www.dmart.in/vegetables']

    def parse(self, response):
        category = response.xpath("//a[@class='nonrwd_only_bc']/text()").get()
        items = response.xpath("//h4//a/text()").getall()
        cost = response.xpath("//p[@class='product-listing--discounted-price ']/text()").getall()



        yield {
            'category': category,
            'items': items,
            'cost':cost
        }
