import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class WikiartImageScraper:
    """
    TODO: Write summary.
    """

    def __init__(self, url, epoch_name, start_index=None, end_index=None):
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