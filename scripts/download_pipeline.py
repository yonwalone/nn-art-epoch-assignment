import os
from src.download_images import WikiartImageScraper
from config import EPOCHS


print("##### Started download pipeline. #####")

for epoch in EPOCHS:
    image_scraper = WikiartImageScraper(epoch_name=epoch, selenium_needed=False)

    image_scraper.log(f"Get images of {epoch} from file.")
    image_scraper.read_images_from_json("images.json")
    image_scraper.log(f"{len(image_scraper.image_list)} already there")

    image_scraper.log(f"Started download for {image_scraper.epoch_name}")
    image_scraper.download_images(0,15000)
    image_scraper.log(f"Finished download for {image_scraper.epoch_name}")

    continue

    #Configuration to get painters filtered from all images
    image_scraper.read_painters_from_json("painters_all.json")
    image_scraper.log(f"{len(image_scraper.painters_dict)} painters found")

    image_scraper.log("Filter painters")
    image_scraper.filter_painter_of_epoch(startIndex=101)

    image_scraper.log(f"{len(image_scraper.painters_dict)} found for epoch")
    image_scraper.save_painters()

    #Configuration to get painters (over images of epoch, important painters)
    image_scraper.log(f"Load painters of featured images of {epoch}.")
    image_scraper.load_all_images()
    image_scraper.get_painters()
    image_scraper.log(f"{len(image_scraper.painters_dict)} painters found.")

    image_scraper.log(f"Load important painters of {epoch}.")
    image_scraper.get_important_painters_of_epoch()
    image_scraper.log(f"{len(image_scraper.painters_dict)} painters found.")
    image_scraper.log(f"Save all painters to file.")
    image_scraper.save_painters()

    # Configuration to get image list from painters in intervals
    image_scraper.read_painters_from_json("painters.json")
    image_scraper.log(f"{len(image_scraper.painters_dict)} painters found")

    image_scraper.log(f"Get images of {epoch} from file.")
    image_scraper.read_images_from_json("images.json")
    image_scraper.log(f"{len(image_scraper.image_list)} already there")

    image_scraper.get_images_from_painters(startIndex=0, endIndex=50)

    image_scraper.log(f"{len(image_scraper.image_list)} images available before clearing.")
    image_scraper.clear_images()
    image_scraper.log(f"{len(image_scraper.image_list)} images now available.")
    image_scraper.save_images()

    # Download images
    image_scraper.read_images_from_json("images.json")
    image_scraper.log(f"{len(image_scraper.image_list)} already there")

    image_scraper.log(f"Started download for {image_scraper.epoch_name}")
    image_scraper.download_images(5)
    image_scraper.log(f"Finished download for {image_scraper.epoch_name}")