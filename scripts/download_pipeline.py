import os
from src.download_images import WikiartImageScraper
from config import EPOCHS


print("##### Started download pipeline. #####")

for epoch in EPOCHS:
    image_scraper = WikiartImageScraper(epoch_name=epoch)

    # image_scraper.log(f"Load painters of featured images of {epoch}.")
    # image_scraper.load_all_images()
    # image_scraper.get_painters()

    # image_scraper.log(f"Load important painters of {epoch}.")
    # image_scraper.get_painters_of_epoch()
    # image_scraper.log(f"Save all painters to file.")

    # image_scraper.save_painters()
    # image_scraper.log(f"Get painters of {epoch} from file.")
    # image_scraper.read_painters_from_json("painters.json")
    # image_count = image_scraper.count_images_via_painters()
    # image_scraper.log(f"{image_scraper.epoch_name}: {image_count} images found.")
    # image_scraper.log(f"Get images of {epoch} from file.")
    # image_scraper.read_images_from_json("images.json")

    # image_scraper.log(f"Get image list from painters of {epoch}.")
    # image_scraper.get_images_from_painters()

    # image_scraper.log("Save images data.")
    # image_scraper.save_images()
    image_scraper.read_images_from_json("images.json")
    image_scraper.log(f"{len(image_scraper.image_list)} images found for {epoch}.")
    image_scraper.remove_image_duplicates()
    image_scraper.log(f"{len(image_scraper.image_list)} images found for {epoch}.")
    image_scraper.save_images()

    # image_scraper.log(f"Started download for {image_scraper.epoch_name}")
    # image_scraper.download_images(5)
    # image_scraper.log(f"Finished download for {image_scraper.epoch_name}")

    ### For loading imag list in parts ###

    #image_scraper.read_painters_from_json("painters.json")
    #image_scraper.log(f"{len(image_scraper.painters_dict)} painters found")

    #image_scraper.read_images_from_json("images.json")
    #image_scraper.log(f"{len(image_scraper.image_list)} images already there")

    #image_scraper.log(f"Get image list from painters of {epoch}.")
    #image_scraper.get_images_from_painters(startIndex=236, endIndex=270)

    #image_scraper.log("Save images data.")
    #image_scraper.save_images()
    #image_scraper.log(f"{len(image_scraper.image_list)} images found for {epoch}.")