from src.download_images import WikiartImageScraper

epoch_name = "expressionism"

image_downloader = WikiartImageScraper(
    url="https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry",
    epoch_name= epoch_name,
    output_dir="C:\\SteffensOrdner\\Programmieren\\Studienarbeit\\nn-art-epoch-assignment\\data",
)

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print(refreshNumber)
refreshNumber = 5
print("refreshNumber: " + str(refreshNumber))

painter_counter = image_downloader.painter_counter()

print("----- START Print -----")
image_downloader.save_to_file("painters_" + epoch_name + ".txt", painter_counter)
print("----- FINISH Print -----")
