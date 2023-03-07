from src.download_images import WikiartImageScraper

epoch_name = "expressionism"

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/" + epoch_name + "?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name= epoch_name,
    output_dir="C:\\SteffensOrdner\\Programmieren\\Studienarbeit\\nn-art-epoch-assignment\\data"
)

image_downloader.start_driver()

print("Read painters from file")
painters_list, count_list = image_downloader.read_authors_from_file("painters_" + epoch_name + ".txt")

img_list = image_downloader.get_images_from_painters(painters_list, epoch_name)
print("Image URLS: " + str(len(img_list)))

print("----- START Download -----")
image_downloader.download_images(10, img_list)
print("----- FINISH Download -----")