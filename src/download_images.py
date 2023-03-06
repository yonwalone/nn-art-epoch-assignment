import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


class WikiartImageScraper:
    """
    TODO: Write summary.
    """

    def __init__(self, url, epoch_name, output_dir, start_index=None, end_index=None):
        """
        TODO: Write docstring.

        Args:
            url (string): Wikiart website URL.
            epoch_name (string): Name of the epoch, e.g. "Expressionism".
            start_index (int, optional): For downloading part of the pictures. Defaults to None.
            end_index (int, optional): For downloading part of the pictures. Defaults to None.
        """
        self.url = url
        self.epoch_name = epoch_name
        self.output_dir = output_dir
        self.start_index = start_index
        self.end_index = end_index
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
    

    def __del__(self):
        """
        Cleans up the webdriver instance when the object is deleted.
        """
        try:
            self.driver.quit()
            print("Webdriver closed.")
        except AttributeError:
            pass
        

    def start_driver(self):
        """
        Initialize and start the Chrome webdriver with the provided options and
        navigate to the URL provided during the initialization of the class.
        """
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)
        print("Webdriver started...")
        time.sleep(3)        
    

    def count_refresh_actions(self):
        """
        Count the number of time the "Load more" button needs to be clicked in order
        to load all the images on the webpage.

        Returns:
            int: The number of times the "Load more" button needs to be clicked.
        """
        # Find the element, that contains the picture and get the total number of pictures.
        informationSections = self.driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
        self.driver.implicitly_wait(50)
        pictureNumber = int(informationSections.pop().text.split(" ").pop())

        # Divide the total number of pictures by 60, which is the default number of pictures loaded per page.
        refreshNumber = int(pictureNumber/60)

        return refreshNumber
    

    def load_more(self, refreshNumber):
        """
        Clicks on the "load more" button 'refreshNumber' times to load more images on the webpage.

        Args:
            refreshNumber (int): The number of times the "load more" button needs to be clicked.
        """
        # Click the "load more" button 'refreshNumber' times to load more images.
        for i in range (0, refreshNumber):
            try:
                self.driver.find_element(By.CLASS_NAME, "masonry-load-more-button").click()
            except:
                self.driver.implicity_wait(5)
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                buttons[0].click()
                i = i - 1
            time.sleep(3)
                
    

    def get_image_urls(self):
        """
        Get the URLs of the images and the epochs in which they belong.
    
        Returns:
            img_url_list (list): List of image URLs.
            img_epoch_list (list): List of epochs in which each image belongs to.
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")
        img_url_list = []
        img_epoch_list = []
        
        # Set the start and end indices for the range of images to scrape.
        if self.start_index is None:
            self.start_index = 0

        if self.end_index is None:
            self.end_index = len(items) - 1

        # Loop through the list of images and extract their URLs and epochs.
        for index in range(self.start_index, self.end_index):
            item = items[index]
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # Scroll to the image and extract its source URL.
                actual_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("arguments[0].scrollIntoView();",img_element )
                img_src = img_element.get_attribute("src")

                epoch_list = []
                self.driver.implicitly_wait(20)

                # Click on the image to open it and extract the epoch information.
                img_element.click()
                self.driver.implicitly_wait(20)
                informationSections = self.driver.find_elements(by=By.CLASS_NAME, value="dictionary-values")
                if len(informationSections) != 0 :
                    information = informationSections[0]
                    epochs = information.find_elements(by=By.TAG_NAME, value="a")
                    for epoch in epochs:
                        epoch_list.append(epoch.text)
                    epoch_list.remove(epoch_list[len(epoch_list)-1])
                else:
                    epoch_list.append(self.epoch_name)
                img_epoch_list.append(epoch_list)

                # Go back to the previous page and wait for it to load.
                self.driver.back()
                self.driver.implicitly_wait(30)

                # Replace the small image URL with the large one and add it to the list.
                img_src = img_src.replace("PinterestSmall", "Large")
                img_url_list.append(img_src)

        return img_url_list, img_epoch_list
    

    def download_images(self, number_of_images, img_url_list, img_epoch_list):
        """
        Download images from a list of image URLs and saves them to the specified output directory.

        Args:
            img_url_list (list of str): List of strings containing the image URL.
            img_epoch_list (list of list of str): A list of lists of strings representing the epochs or periods
                                                  associated with each image URL in img_url_list. The outer list
                                                  should have the same length as img_url_list, and each inner list
                                                  can have any number of elements.

        Raises:
            ValueError: If an image URL does not contain a valid image extension.
        """
        # Loop through the image URLs and download the images.
        for i in range(len(img_url_list)):
            # Check if we have already downloaded the maximum number of images.
            if i >= number_of_images:
                pass
            else:
                # Set filename from url if possible otherwise use string of i.
                epochs = img_epoch_list[i]
                epoch_string = "-".join(epochs) + "-"
                try:
                    reg_results = re.search(r"images/([^/]+)\.(jpg|jpeg|png)", img_url_list[i])
                    if reg_results is None:
                        raise ValueError("Image URL does not contain a valid image extension")

                    local_file_name = reg_results.group(1).replace("/", "_").replace("-", ".")
                    local_file_name = epoch_string + local_file_name
                except Exception as e:
                    # If there is an error with the regex, use the index i as the filename.
                    local_file_name = epoch_string + str(i)

                # Download picture from url.
                try:
                    urllib.request.urlretrieve(img_url_list[i], os.path.join(self.output_dir, f"{local_file_name}.jpg"))
                except Exception as e:
                     # If the initial download fails, try removing any suffixes from the image URL.
                    try:
                        img_url = img_url_list[i].replace("!Large.jpg", "").replace("!Large.png", "").replace("!Large.jpeg", "")
                        urllib.request.urlretrieve(img_url, os.path.join(self.output_dir, f"{local_file_name}.jpg"))
                    except Exception as e:
                        # If the download still fails, print an error message and move on to the next image.
                        print(f"Error downloading image from URL: {img_url_list[i]}")
                        print(e)
                        pass