import os
from src.download_images import WikiartImageScraper
from config import EPOCHS


print("##### Started download pipeline. #####")

for epoch in EPOCHS:
    image_scraper = WikiartImageScraper(epoch_name=epoch)
    image_scraper.load_all_pictures()
    image_scraper.get_painters()
    image_count = image_scraper.count_images_via_painters()
    print(f"{image_scraper.epoch_name}: {image_count} images found.")