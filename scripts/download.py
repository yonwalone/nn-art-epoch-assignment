import os
from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name="Expressionism",
)

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print("refreshNumber: " + str(refreshNumber))

img_url_list, img_epoch_list = image_downloader.get_image_urls()
print(img_url_list)
print(img_epoch_list)
