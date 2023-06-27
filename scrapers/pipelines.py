import logging
from collections import defaultdict

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.spiders import Spider
from scrapy.utils.misc import md5sum

from scrapers.azure_helpers import upload_blob
from scrapers.items import PropertyItem

# Not process duplicates
class DuplicatesPipeline:
    def __init__(self):
                self.ids_seen = set()

    def process_item(self, item, spider: Spider) -> dict:
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item

# Not usable
class ItemLimit:
    def __init__(self, max_items_per_label: int, label_field: str):
        self.label_counts = defaultdict(int)
        self.max_items_per_label = max_items_per_label
        self.label_field = label_field

    def process_item(self, item, spider: Spider) -> dict:
        adapter = ItemAdapter(item)
        label = adapter[self.label_field]
        if self.label_counts[label] >= self.max_items_per_label:
            raise DropItem(f"Reached max number of items for label {label}")
        else:
            self.label_counts[label] += 1
            return item

    @classmethod
    def from_crawler(cls, crawler):
        try:
            max_items_per_label = crawler.settings["max_items_per_label"]
            label_field = crawler.settings["label_field"]
        except KeyError as exc:
            logging.error(
                "max_items_per_label or label_field settings not found in the crawler"
                "settings. You need to set them for the ItemLimit pipeline to work.\n"
                f"{exc}"
            )
        return cls(max_items_per_label, label_field)

# Create string for image name and upload it to Blob in Azure
class AzureImagesPipeline(ImagesPipeline):
    def image_downloaded(self, response, request, info, *, item):
        item_id = item["id"].strip()
        item_propertytype = item["property_type"].strip()
        item_propertyrooms = item["property_rooms"].strip()
        item_squaremeters = item["square_meters"].strip()
        newpath = "_"+item_id+"_"+item_propertytype+"_"+item_propertyrooms+"_"+item_squaremeters
    
        checksum = None
        for path, _, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            upload_blob("images/"+checksum+newpath+".jpg", buf)
        return checksum
