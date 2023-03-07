from src.download_images import WikiartImageScraper

epoch_name = "expressionism"
output_dir = "C:\\SteffensOrdner\\Programmieren\\Studienarbeit\\nn-art-epoch-assignment\\data"

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name= epoch_name,
    output_dir= output_dir
)

image_downloader.start_driver()

print("Read painters from file")
painters_list, count_list = image_downloader.read_authors_from_file("painters_" + epoch_name + ".txt")

print("----- Calculate Reachable Image Count -----")
img_count = image_downloader.get_count_of_available_images_from_authors(painters_list= painters_list, epoch= epoch_name)
print(str(img_count) + " Pictures Reachable")