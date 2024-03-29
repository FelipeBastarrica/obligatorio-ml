import scrapy

# Property Items defined
class PropertyItem(scrapy.Item):
    id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    property_type = scrapy.Field()
    property_rooms = scrapy.Field()
    square_meters = scrapy.Field()

