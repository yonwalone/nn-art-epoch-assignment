from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name="Expressionism",
    output_dir="/Users/SOK1USH/Documents/nn-art-epoch-assignment/data"
)

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print("refreshNumber: " + str(refreshNumber))

img_url_list, img_epoch_list = image_downloader.get_image_urls()
print("Image URLS: " + str(len(img_url_list)))

print("----- START Download -----")
image_downloader.download_images(10, img_url_list, img_epoch_list)
print("----- FINISH Download -----")

