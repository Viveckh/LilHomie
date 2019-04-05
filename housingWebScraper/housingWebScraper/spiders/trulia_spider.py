#############################
# Trulia Spider (Entry Point)
# Author: (EJ) Vivek Pandey
# Last Modified: 03/05/2019
#############################

import scrapy
from housingWebScraper.itemloaders import TruliaItemsLoader

def extract_with_css(response, query):
    return response.css(query).get(default='').strip()

class TruliaSpider(scrapy.Spider):
    name = 'trulia'
    start_urls = [
        'https://www.trulia.com/property-sitemap/',
    ]

    def parse(self, response):
        for state in response.css('ul.all-states > li'):
            # For now only extract data for New York tri states, remove this condition if you want to crawl data for all states
            stateName = extract_with_css(state, 'a.clickable::text')
            if "New Jersey" not in stateName and "New York" not in stateName and "Connecticut" not in stateName:
                continue

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
                    yield response.follow(properties_page_url, self.parse_property)

    def parse_properties(self, response):
        for property in response.css('ul.all-properties > li'):
            property_page_url = extract_with_css(property, 'a.clickable::attr("href")')
            if property_page_url is not None:
                yield response.follow(property_page_url, self.parse_property)

    def parse_property(self, response):
        if extract_with_css(response, '#propertySummary .addressContainer h1 div[data-role="address"]::text') is not None:
            yield TruliaItemsLoader.parse_property(self, response=response)
            
            # This has to be handled separately for different property page formats that trulia has
            for event in response.css('div[data-auto-test-id="home-details-price-history"] > div[data-role="contentWithToggle"]'):
                if extract_with_css(event, 'div[data-role="toggleArrow"] > div:last-child::text') == 'Sold':
                    yield TruliaItemsLoader.parse_transaction(self, transaction=event, property_url=response.request.url)

    