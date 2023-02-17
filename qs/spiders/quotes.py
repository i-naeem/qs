import scrapy
from qs.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    def start_requests(self):
        url = "http://quotes.toscrape.com/"
        tag = getattr(self, 'tag', None)
        if tag:
            url = url + '/tag/' + tag

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quote_divs = response.css('div.quote')

        for quote_div in quote_divs:
            item = QuoteItem()
            item['text'] = quote_div.css('span.text::text').get()
            item['tags'] = quote_div.css('.tag::text').getall()
            item['author'] = quote_div.css('.author::text').get()

            yield item

        next_page = response.css('ul.pager .next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
