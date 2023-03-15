from src.download_images import WikiartImageScraper

image_downloader = WikiartImageScraper(
    epoch_name="expressionism",
    start_index= 5,
    end_index= 30
)

image_downloader.start_driver()

refreshNumber = image_downloader.count_refresh_actions()
print(refreshNumber) # Test
refreshNumber = 2   # Test
print("refreshNumber: " + str(refreshNumber))

img_list = image_downloader.get_image_list()
print("Image URLS: " + str(len(img_list)))

print("----- START Download -----")
image_downloader.download_images(10, img_list)
print("----- FINISH Download -----")
