from typing import Iterator

from requests.utils import requote_uri
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapers.azure_helpers import append_file_to_blob
from scrapers.items import PropertyItem


class GallitoSpider(CrawlSpider):
    name = "gallito"
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
        "FEEDS": {
            "properties_gallito.jl": {"format": "jsonlines"}
        },
        "max_items_per_label": 15,
        "label_field": "property_type",
        "CLOSESPIDER_ITEMCOUNT": 300,
    }
    start_urls = [
        "https://www.gallito.com.uy/inmuebles/casas!cant=80",  # !cant=80
        "https://www.gallito.com.uy/inmuebles/apartamentos!cant=80",  # !cant=80
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    [
                        r"\/inmuebles\/casas\?pag=\d+",  # !cant=80\?pag=\d+
                        r"\/inmuebles\/apartamentos\?pag=\d+",  # !cant=80\?pag=\d+
                    ]
                )
            )
        ),
        Rule(LinkExtractor(allow=(r"-\d{8}$")), callback="parse_property"),
    )

    def parse_property(self, response: HtmlResponse) -> Iterator[dict]:
        def get_with_css(query: str) -> str:
            return response.css(query).get(default="").strip()

        def extract_with_css(query: str) -> list[str]:
            return [
                line for elem in response.css(query).extract() if (line := elem.strip())
            ]

        # property details
        property_id = get_with_css("#HfCodigoAviso::attr('value')")
        img_urls = get_with_css("#HstrImg::attr('value')")
        img_urls = [img for img in img_urls.split(",") if img]
        possible_types = {
            "casa": "HOUSE",
            "apartamento": "APARTMENT",
        }
        possible_rooms = {
            "monoambiente": "0D",
            "1 dormitorio": "1D",
            "2 dormitorios": "2D",
            "3 dormitorios": "3D",
            "4 dormitorios": "4D",
            "más de 4 dormitorios": "+4D",
        }

        # every property has this fixed list of details on gallito
        fixed_details = extract_with_css("div.iconoDatos + p::text")
        property_type = possible_types[fixed_details[0].lower()] 
        property_rooms = possible_rooms[fixed_details[3].lower()]  
        square_meters = fixed_details[5].lower().replace(" ","") 

        property = {
            "id": property_id,
            "image_urls": img_urls,
            "source": "gallito",
            "url": requote_uri(response.request.url),
            "link": requote_uri(response.request.url),
            "property_type": property_type,
            "property_rooms": property_rooms,
            "square_meters": square_meters
        }
        yield PropertyItem(**property)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GallitoSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s", spider.name)
        for uri, _ in self.settings.getdict("FEEDS").items():
            append_file_to_blob(uri)
