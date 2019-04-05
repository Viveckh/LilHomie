#############################
# Custom Exporters
# Author: (EJ) Vivek Pandey
# Last Modified: 03/05/2019
#############################

from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter

"""
    This exporter works when you
        add a new option in FEED_EXPORTERS within settings.py pointing to this class
        add a CSV_DELIMITER key in settings.py
    
    Then, start scrapy with following command
    scrapy crawl spidername --set FEED_URI=output.csv --set FEED_FORMAT=custom_csv
"""
class CsvOptionRespectingItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        super(CsvOptionRespectingItemExporter, self).__init__(*args, **kwargs)