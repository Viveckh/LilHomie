import scrapy

def extract_with_css(response, query):
    return response.css(query).get(default='').strip()

class TruliaSpider(scrapy.Spider):
    name = 'trulia'
    start_urls = [
        'https://www.trulia.com/property-sitemap/',
    ]

    def parse(self, response):
        for state in response.css('ul.all-states > li'):
            counties_page_url = extract_with_css(state, 'a.clickable::attr("href")')
            if counties_page_url is not None:
                yield response.follow(counties_page_url, self.parse_counties)

    def parse_counties(self, response):
        for county in response.css('ul.all-counties > li'):
            zipcodes_page_url = extract_with_css(county, 'a.clickable::attr("href")')
            if zipcodes_page_url is not None:
                yield response.follow(zipcodes_page_url, self.parse_zipcodes)

    def parse_zipcodes(self, response):
        for zipcode in response.css('ul.all-zip-codes > li'):
            streets_page_url = extract_with_css(zipcode, 'a.clickable::attr("href")')
            if streets_page_url is not None:
                yield response.follow(streets_page_url, self.parse_streets)

    def parse_streets(self, response):
        for street in response.css('ul.all-streets > li'):
            properties_page_url = extract_with_css(street, 'a.clickable::attr("href")')
            if properties_page_url is not None:
                # If there is only a single property record for a street, the property url is in href instead of the properties sitemap url
                if "trulia.com/p/" not in properties_page_url:
                    yield response.follow(properties_page_url, self.parse_properties)
                else:
                    #yield response.follow(properties_page_url, self.parse_property)
                    yield {
                        'url': properties_page_url
                    }    

    def parse_properties(self, response):
        for property in response.css('ul.all-properties > li'):
            property_page_url = extract_with_css(property, 'a.clickable::attr("href")')
            yield {
                'url': property_page_url
            }

    def parse_property(self, response):
        yield {
            'name': extract_with_css(response, 'a.clickable::text'),
            'url': extract_with_css(response, 'a.clickable::attr("href")'),
        }

    