from src.download_images import WikiartImageScraper


def download_from_epoch(epoch_name):
    """_summary_

    Args:
        epoch_name (_type_): _description_
    """
    image_downloader = WikiartImageScraper(
        epoch_name=epoch_name,
        start_index= 5,
        end_index= 30
    )

    image_downloader.start_driver()

    refresh_counter= image_downloader.count_refresh_actions()

    print("refresh_counter: " + str(refresh_counter))

    img_list = image_downloader.get_image_list()
    print("Image URLS: " + str(len(img_list)))

    print("----- START Download -----")
    image_downloader.download_images(10, img_list)
    print("----- FINISH Download -----")


def download_from_painters(epoch_name):
    """_summary_

    Args:
        epoch_name (_type_): _description_
    """
    image_downloader = WikiartImageScraper(epoch_name=epoch_name)

    image_downloader.start_driver()

    print("Read painters from file")
    painters_list, count_list = image_downloader.read_painters_from_file(
        "painters_" + epoch_name + ".txt")

    img_list = image_downloader.get_images_from_painters(painters_list, epoch_name)
    print("Image URLS: " + str(len(img_list)))

    print("----- START Download -----")
    image_downloader.download_images(10, img_list)
    print("----- FINISH Download -----")
