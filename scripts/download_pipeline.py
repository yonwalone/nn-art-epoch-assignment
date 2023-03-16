import os
from src.download_images import WikiartImageScraper
from config import EPOCHS


print("##### Started download pipeline. #####")

for epoch in EPOCHS:
    image_scraper = WikiartImageScraper(epoch_name=epoch)
    # image_scraper.load_all_pictures()
    # image_scraper.get_painters()
    # image_scraper.save_painters()
    image_scraper.read_painters_from_json("painters.json")
    # image_count = image_scraper.count_images_via_painters()
    # print(f"{image_scraper.epoch_name}: {image_count} images found.")
    image_scraper.get_images_from_painters()
    print(f"Started download for {image_scraper.epoch_name}")
    image_scraper.download_images(5)
    print(f"Finished download for {image_scraper.epoch_name}")