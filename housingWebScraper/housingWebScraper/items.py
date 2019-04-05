# -*- coding: utf-8 -*-
#############################
# Item Definitions
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
#
# Author: (EJ) Vivek Pandey
# Last Modified: 03/05/2019
#############################

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
    lot_size = scrapy.Field()
    no_of_bedrooms = scrapy.Field()
    no_of_baths = scrapy.Field()
    no_of_stories = scrapy.Field()
    parking_type = scrapy.Field()
    no_of_parking_spaces = scrapy.Field()
    heating_type = scrapy.Field()
    basement_type = scrapy.Field()
    exterior_type = scrapy.Field()
    tax_year = scrapy.Field()
    tax_amount = scrapy.Field()

class Transaction(scrapy.Item):
    property_url = scrapy.Field()
    recording_date = scrapy.Field()
    contract_date = scrapy.Field()
    price = scrapy.Field()
    transaction_type = scrapy.Field()
    document_type = scrapy.Field()
    county_transfer_tax = scrapy.Field()
    total_transfer_tax = scrapy.Field()
    

