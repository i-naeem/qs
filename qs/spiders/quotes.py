import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quote_divs = response.xpath('//div[normalize-space(@class)="quote"]')

        for quote_div in quote_divs:
            author = quote_div.css('.author::text').get().strip()
            quote = quote_div.css('.text::text').get().strip()
            tags = quote_div.css('.tags .tag::text').getall()

            yield {"author": author, "quote": quote, "tags": tags}
