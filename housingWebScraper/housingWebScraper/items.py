# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousingwebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Property(scrapy.Item):
    property_url = scrapy.Field()
    property_type = scrapy.Field()
    built_year = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    area_sqft = scrapy.Field()
    lot_size_sqft = scrapy.Field()
    no_of_stories = scrapy.Field()
    no_of_bedrooms = scrapy.Field()
    no_of_baths = scrapy.Field()
    parking_type = scrapy.Field()
    no_of_parking_spaces = scrapy.Field()
    heating_type = scrapy.Field()
    basement_type = scrapy.Field()
    exterior_type = scrapy.Field()
    tax_year = scrapy.Field()
    tax_amount = scrapy.Field()
    txn_recording_date = scrapy.Field()
    txn_contract_date = scrapy.Field()
    txn_price = scrapy.Field()
    txn_type = scrapy.Field()
    txn_document_type = scrapy.Field()
    txn_county_transfer_tax = scrapy.Field()
    txn_total_transfer_tax = scrapy.Field()
    

