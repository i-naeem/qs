import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):

        yield from response.follow_all(css=".author + a", callback=self.parse_author)

        next_page = response.css('ul.page .next a::attr(href)').getall()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        name = response.css('.author-title::text').get().strip()
        dob = response.css('.author-born-date::text').get().strip()
        dob_location = response.css(
            '.author-born-location::text').get().strip()
        about = response.css('.author-description::text').get().strip()

        yield {
            "dob": dob,
            "name": name,
            "about": about,
            "dob_location": dob_location,
        }
