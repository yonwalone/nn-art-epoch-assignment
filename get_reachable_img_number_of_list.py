from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(epoch_name="expressionism")

image_downloader.start_driver()

print("Read painters from file")
painters_list, count_list = image_downloader.read_painters_from_file(
    "painters_" + epoch_name + ".txt")

print("----- Calculate Reachable Image Count -----")
img_count = image_downloader.get_count_of_available_images_from_authors(
    painters_list=painters_list, epoch=epoch_name)
print(str(img_count) + " Pictures Reachable")
