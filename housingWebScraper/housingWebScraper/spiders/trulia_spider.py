import scrapy

class StatesSpider(scrapy.Spider):
    name = 'trulia'
    start_urls = [
        'https://www.trulia.com/property-sitemap/',
    ]

    def parse(self, response):
        for state in response.css('ul.all-states > li'):
            yield {
                'name': state.css('a.clickable::text').get(),
                'url': state.css('a.clickable::attr("href")').get(),
            }

        '''
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        '''