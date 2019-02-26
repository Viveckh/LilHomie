from scrapy.loader import ItemLoader
from housingWebScraper.items import Property
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join
import re

clean_text = Compose(MapCompose(lambda v: v.strip()), Join())   
to_int = Compose(TakeFirst(), int)

def extract_with_css(response, query):
    return response.css(query).get(default='').strip()

class TruliaPropertyLoader(ItemLoader):

    default_item_class = Property
    default_output_processor = clean_text

    def parse(self, response):
        loader = TruliaPropertyLoader(selector=response)
        
        #Populate the property url to view it later
        loader.add_value('property_url', response.request.url)

        # There are pages in multiple formats, we'll have to use different parsers for each
        if extract_with_css(response, '#propertySummary .addressContainer h1 div[data-role="address"]::text') is not None:
            # Populate address fields
            loader.add_css('address', '#propertySummary .addressContainer h1 div[data-role="address"]::text')

            city_state_zip = extract_with_css(response, '#propertySummary .addressContainer h1 span[data-role="cityState"]::text')
            # Extracts city, state and zip from strings like "Caldwell, NJ 07430" or "New Haven, CT 98930"
            res = re.findall(r"(?P<city>[A-Za-z\s]*),\s+(?P<state>[A-Z]*)\s+(?P<zip_code>[0-9]*)", city_state_zip)
            if res:
                (city, state, zip_code) = res[0]
                loader.add_value('city', city)
                loader.add_value('state', state)
                loader.add_value('zip_code', zip_code)

            # Populate property details from the randomized list
            for entry in response.css('div[data-auto-test-id="home-detail"] div[data-auto-test-id="home-details-overview"] ul li'):
                raw_property_detail = extract_with_css(entry, '::text')

                # Extract built year if pattern matches - eg. Built in 1995
                match = re.match(r"\s*Built\s+in\s+(?P<built_year>[0-9]+)\s*$", raw_property_detail)
                if match is not None:
                    loader.add_value('built_year', match.group('built_year'))

                # Extract no of bedrooms if matches - eg. 3.5 Beds
                match = re.match(r"\s*(?P<no_of_bedrooms>[0-9\.]+)\s+Beds\s*$", raw_property_detail)
                if match is not None:
                    loader.add_value('no_of_bedrooms', match.group('no_of_bedrooms'))
                
                # Extract no of baths if matches - eg. 3 Baths
                match = re.match(r"\s*(?P<no_of_baths>[0-9\.]+)\s+Baths\s*$", raw_property_detail)
                if match is not None:
                    loader.add_value('no_of_baths', match.group('no_of_baths'))

                # Extract area sqft if matches - eg. 2,9863.5 sqft
                match = re.match(r"\s*(?P<area_sqft>[0-9,\.]+)\s+sqft\s*$", raw_property_detail)
                if match is not None:
                    loader.add_value('area_sqft', match.group('area_sqft'))
        
            # Populate tax fields
            loader.add_css('tax_year', 'div[data-auto-test-id="home-detail"] > div:nth-last-of-type(1) > .mbm > :nth-child(1) :nth-child(2)::text')
            loader.add_css('tax_amount', 'div[data-auto-test-id="home-detail"] > div:nth-last-of-type(1) > .mbm > :nth-child(2) :nth-child(2)::text')

        return loader.load_item()