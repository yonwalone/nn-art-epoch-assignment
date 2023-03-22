import os
from src.download_images import WikiartImageScraper
from config import EPOCHS


print("##### Started download pipeline. #####")

for epoch in EPOCHS:
    image_scraper = WikiartImageScraper(epoch_name=epoch)

    print(f"Load painters of featured images of {epoch}.")
    image_scraper.load_all_images()
    image_scraper.get_painters()

    print(f"Load important painters of {epoch}.")
    image_scraper.get_painters_of_epoch()
    print(f"Save all painters to file.")

    image_scraper.save_painters()
    image_scraper.read_painters_from_json("painters.json")
    # image_count = image_scraper.count_images_via_painters()
    # print(f"{image_scraper.epoch_name}: {image_count} images found.")

    print(f"Get image list from painters of {epoch}.")
    image_scraper.get_images_from_painters()

    print("Save images data.")
    image_scraper.save_images()
    image_scraper.read_images_from_json("images.json")
    print(f"{len(image_scraper.image_list)} images found for {epoch}.")

    print(f"Started download for {image_scraper.epoch_name}")
    image_scraper.download_images(5)
    print(f"Finished download for {image_scraper.epoch_name}")

    ### For loading imag list in parts ###

    #image_scraper.read_painters_from_json("painters.json")
    #print(f"{len(image_scraper.painters_dict)} painters found")

    #image_scraper.read_images_from_json("images.json")
    #print(f"{len(image_scraper.image_list)} images already there")

    #print(f"Get image list from painters of {epoch}.")
    #image_scraper.get_images_from_painters(startIndex=236, endIndex=270)

    #print("Save images data.")
    #image_scraper.save_images()
    #print(f"{len(image_scraper.image_list)} images found for {epoch}.")