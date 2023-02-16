import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quote_divs = response.css('div.quote')

        for quote_div in quote_divs:
            yield {"text": quote_div.css('span.text::text').get()}

        next_page = response.css('ul.pager .next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
