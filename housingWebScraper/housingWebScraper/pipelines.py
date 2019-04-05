# -*- coding: utf-8 -*-
#############################
# Pipelines
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
# Author: (EJ) Vivek Pandey
# Last Modified: 03/05/2019
#############################

from scrapy import signals
from scrapy.conf import settings
from housingWebScraper.exporters import CsvOptionRespectingItemExporter

def item_type(item):
    return type(item).__name__

class HousingwebscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MultiCSVItemPipeline(object):
    SaveTypes = ['Property','Transaction']

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.files = dict([ (name, open(settings.get('CSV_OUTPUT_FOLDER') + name + '.csv','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvOptionRespectingItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
