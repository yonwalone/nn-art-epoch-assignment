#from src.download_images import WikiartImageScraper
from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name="Expressionism",
    output_dir="C:\\SteffensOrdner\\Programmieren\\Studienarbeit\\nn-art-epoch-assignment\\data",
    start_index= 5,
    end_index= 30
)

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print(refreshNumber)
refreshNumber = 2
print("refreshNumber: " + str(refreshNumber))

img_list = image_downloader.get_image_urls()
print("Image URLS: " + str(len(img_list)))

print("----- START Download -----")
image_downloader.download_images(10, img_list)
print("----- FINISH Download -----")

