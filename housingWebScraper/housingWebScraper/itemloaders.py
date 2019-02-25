from scrapy.loader import ItemLoader
from housingWebScraper.items import Property
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join

clean_text = Compose(MapCompose(lambda v: v.strip()), Join())   
to_int = Compose(TakeFirst(), int)

class TruliaPropertyLoader(ItemLoader):

    default_item_class = Property
    default_output_processor = clean_text

    def parse(self, response):
        loader = TruliaPropertyLoader(selector=response)
        loader.add_css('address', '#propertySummary .addressContainer h1 div[data-role="address"]::text')
        loader.add_css('city', '#propertySummary .addressContainer h1 span[data-role="cityState"]::text')
        return loader.load_item()