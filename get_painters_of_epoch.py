from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(epoch_name="expressionism")

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print(refreshNumber) # Test
refreshNumber = 5 # Test
print("refreshNumber: " + str(refreshNumber))

print("Extracting painters")
painter_counter = image_downloader.painter_counter()

print("----- START Print -----")
image_downloader.save_to_file("painters_" + epoch_name + ".txt", painter_counter)
print("----- FINISH Print -----")
