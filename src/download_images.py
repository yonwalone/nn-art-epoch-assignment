import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from collections import Counter
import json
from config import PROJECT_ROOT
from src.image import Image



class WikiartImageScraper:
    """
    Web scraper that uses Selenium and ChromeDriver to extract images from the Wikiart website 
    based on the provided URL and epoch name.
    """

    def __init__(self, epoch_name, start_index=None, end_index=None):
        """
        Initializes a new WikiartImageScraper object.

        Args:
            url (string): Wikiart website URL.
            epoch_name (string): Name of the epoch, e.g. "expressionism".
            start_index (int, optional): For downloading part of the pictures. Defaults to None.
            end_index (int, optional): For downloading part of the pictures. Defaults to None.
        """
        self.epoch_name = epoch_name
        self.start_index = start_index
        self.end_index = end_index
        self.url = f"https://www.wikiart.org/en/paintings-by-style/{epoch_name}?select=featured#!#filterName:featured,viewType:masonry"
        self.output_dir = os.path.join(PROJECT_ROOT, "data", epoch_name)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.painters_dict = {}
        self.image_list = []

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.start_driver()

    def __del__(self):
        """
        Cleans up the webdriver instance when the object is deleted.
        """
        try:
            self.driver.close()
            self.driver.quit()
            print("Webdriver closed.")
        except AttributeError:
            pass

    def navigate_to_url(self, url):
        """
        Navigate the webdriver to the specified URL.

        Args:
            url (string): The URL to navigate to.
        """
        self.driver.get(url)

    def start_driver(self):
        """
        Initializes and start the Chrome webdriver with the provided options and
        navigate to the URL provided during the initialization of the class.
        """
        self.driver = webdriver.Chrome(options=self.options)
        self.navigate_to_url(self.url)
        print("Webdriver started...")
        time.sleep(3)

    def count_refresh_actions(self):
        """
        Count the number of time the "Load more" button needs to be clicked in order
        to load all the images on the webpage.

        Returns:
            int: The number of times the "Load more" button needs to be clicked.
        """
        # Find the element, that contains the total number of pictures and saves it.
        informationSections = self.driver.find_elements(
            by=By.CLASS_NAME, value="count.ng-binding")
        self.driver.implicitly_wait(50)
        pictureCount = int(informationSections.pop().text.split(" ").pop())

        # Divide the total number of pictures by 60, which is the default number of pictures loaded per page.
        refreshCount = int(pictureCount/60)

        # Correct refresh number because at the beginning the first pictures are visible.
        refreshCount = refreshCount - 2

        return refreshCount

    def load_more(self, refreshCount):
        """
        Clicks on the "load more" button 'refreshCount' times to load more images on the webpage.

        Args:
            refreshCount (int): The number of times the "load more" button needs to be clicked.
        """
        # Click the "load more" button 'refreshCount' times to load more images.
        for i in range(0, refreshCount):
            try:
                # The "load more" button may not be found
                self.driver.find_element(
                    By.CLASS_NAME, "masonry-load-more-button").click()
            except:
                # Handle popups
                self.driver.implicitly_wait(5)
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                buttons[0].click()
                i = i - 1
            time.sleep(5)

    def get_painter_from_url(self, img_src):
        """
        Gets painter of a picture.

        Args:
            img_src (string): Name of the image path.

        Returns:
            string: Name of painter of the image
        """
        try:
            # Looks for a string that starts with "images/",
            # then has one or more characters followed by a "/",
            # and returns the entire substring that matches this pattern.
            image_path = re.search("images/(.+?)/", img_src)[0]
            painter_name = image_path.split("/")[1]
        except:
            painter_name = "no_painter"

        return painter_name


    def get_epochs(self, img_element):
        """
        Gets the epochs of an image element.

        Args:
            img_element (object): HTML element of the image.

        Returns:
            list of strings: Epochs of the image.
        """
        epoch_list = []
        self.driver.implicitly_wait(20)

        # Click on the image to open it and extract the epoch information.
        protected = True
        while protected:
            try:
                img_element.click()
                self.driver.implicitly_wait(20)
                protected = False
            except:
                buttons = self.driver.find_elements(by=By.TAG_NAME, value="button")
                buttons[0].click()
        

        try:
            # Gets Element where the epochs are listed
            information = self.driver.find_elements(
                by=By.CLASS_NAME, value="dictionary-values")[0]
            epochs = information.find_elements(by=By.TAG_NAME, value="a")
            for epoch in epochs:
                epoch_list.append(epoch.text)
            # Last element gets removed because it isn't an epoch
            epoch_list.remove(epoch_list[len(epoch_list)-1])
        except:
            epoch_list.append(self.epoch_name)

        # Go back to the previous page and wait for it to load.
        self.driver.back()
        self.driver.implicitly_wait(30)

        return epoch_list

    def get_image_list(self, painter=None):
        """
        Gets the URLs of the images and the epochs in which they belong.

        Args:
            painter (string): name of the painter if driver is on a painter site.        
        Returns:
            img_list (list): List of image urls
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(
            By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")
        img_list = []

        print(f"{len(items)} images from {painter} found.")
        if len(items) == 20 and painter != None:
            print("Not all images may be available: " + str(painter))
            return []

        # Loop through the list of images and extract their URLs and epochs.
        for item in items:
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # Scroll to the image and extract its source URL.
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", img_element)
                img_src = img_element.get_attribute("src")
                try:
                    epoch_list = self.get_epochs(img_element)
                except:
                    print(f"Could't get the image of soure: {img_src}")
                    epoch_list = [self.epoch_name]
                # Replace the small image URL with the large one and add it to the list.
                img_src = img_src.replace("PinterestSmall", "Large")

                # Appends the created Image to the img list
                img_list.append(Image(url=img_src, epochs=epoch_list))

        return img_list

    def get_painters(self):
        """
        Get the painters of the featured images.

        Returns:
            None
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(
            By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")

        # Loop through the list of images and extract their URLs and epochs.
        for item in items:
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # Scroll to the image and extract its source URL.
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", img_element)
                img_src = img_element.get_attribute("src")

                # Extract painter out from url
                painter = self.get_painter_from_url(img_src)

                if painter in self.painters_dict:
                    self.painters_dict[painter] += 1
                else:
                    self.painters_dict[painter] = 1

    def painter_counter(self):
        """
        Get the Counter of the painters from the featured painters of the epoch

        Returns:
            counter : Counter object of the painters from the featured painters of the epoch
        """

        painter_list = self.get_painters()
        counter = Counter(painter_list)
        return counter

    def save_to_file(self, file_name, dict):
        """
        Save object as text to file 

        Parameter:
            file_name : name of file to write in
            object: object that should be written as text
        """
        with open(os.path.join(self.output_dir, file_name), "w") as f:
            json.dump(dict, f)

    def save_painters(self):
        """_summary_
        """
        self.save_to_file("painters.json", self.painters_dict)

    def read_painters_from_json(self, file_name):
        """
        Get list of painters and the count of their featured pictures from file

        Parameter:
            file_name : name of file with counter object of painters

        Returns:
            painter_list (list) : painters named in file
            image_count_list (list)
        """

        with open(os.path.join(self.output_dir, file_name), "r") as file:
            painters_dict = json.load(file)
        
        self.painters_dict = painters_dict

    def count_images_via_painters(self):
        """
        Get count of pictures reachable from the painters of epoch

        Parameter:
            painters_list (list) : names of painters
            epoch (String): name of epoch

        Returns:
            image_count : count of reachable images
        """
        total_image_count = 0
        for painter in self.painters_dict:
            if not self.is_painter_available(painter=painter):
                continue
            try:
                painter_image_count = 0

                # Get Url of the pictures from the author of the chosen epoch
                self.navigate_to_url("https://www.wikiart.org/en/" +
                                    painter + "/all-works#!#filterName:Style_" + self.epoch_name + ",resultType:masonry")
                self.driver.implicitly_wait(10)
                # TODO: eventuell WebDriverWait.until verwenden

                # Find the load more button
                informationSections = self.driver.find_elements(
                    by=By.CLASS_NAME, value="count.ng-binding")
                self.driver.implicitly_wait(5)

                # Check if theres a load more button
                if informationSections[0].text != "":
                    # Read the picture number from the button
                    painter_image_count = int(
                        informationSections.pop().text.split(" ").pop())
                else:
                    # Count images dispayed on the screen
                    html_pictures_list = self.driver.find_elements(
                        By.CLASS_NAME, "wiki-masonry-container")
                    items = html_pictures_list[0].find_elements(
                        By.TAG_NAME, "li")
                    for item in items:
                        img_elements = item.find_elements(By.TAG_NAME, "img")
                        painter_image_count = painter_image_count + \
                            int(len(img_elements))

                # Add found images from the author to total count
                total_image_count = total_image_count + painter_image_count
            except:
                print("Images of " +
                    str(painter) + " not reachable")

        return total_image_count

    def get_images_from_painters(self):
        """
        Get the image URLs of the painters

        Parameter:
            painters_list (list) : names of painters
            epoch (String): name of epoch

        Returns:
            None
        """

        for painter in self.painters_dict:
            self.image_list.append(self.get_images_from_painter(painter))

    def is_painter_available(self, painter):
        """_summary_

        Args:
            painter (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            # Get Url
            self.navigate_to_url(f"https://www.wikiart.org/en/{painter}")
            self.driver.implicitly_wait(1)
        except:
            print(f"Cant find page of {painter}.")
            return  False
        
        privacy_hint = self.driver.find_elements(by=By.CLASS_NAME, value="wiki-layout-restricted-msg-wrapper")

        if len(privacy_hint) > 0:
            return False

        return True

    def get_images_from_painter(self, painter):
        """_summary_

        Args:
            painter (_type_): _description_
            epoch (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not self.is_painter_available(painter=painter):
            return []
        
        try:
            # Get Url
            self.navigate_to_url("https://www.wikiart.org/en/" + painter + "/all-works#!#filterName:Style_" + self.epoch_name + ",resultType:masonry")
            self.driver.implicitly_wait(40)
        except:
            print(f"Cant find URL of {painter}.")
            return []
        
        try:
            # Find Load More Button
            load_more_button = self.driver.find_elements(
                by=By.CLASS_NAME, value="masonry-load-more-button")[0]
            rawCountText = load_more_button.find_elements(
                by=By.CLASS_NAME, value="count")[0].text

            # If not all Pictures visible click onto load more button
            if rawCountText != "":
                label = self.driver.find_elements(
                    by=By.CLASS_NAME, value="count.ng-binding")
                self.driver.implicitly_wait(5)
                pictureNumber = int(label.pop().text.split(" ").pop())

                # Calculate number of needed load more clicks
                refresh_number = (pictureNumber - 20) / 60
                refresh_number = int(refresh_number) + 1

                self.load_more(refresh_number)
        except:
            print(f"Images of painter {painter} not reachable.")
            return []

        return self.get_image_list(painter=painter)

    def download_images(self, number_of_images):
        """
        Download images from a list of image URLs and saves them to the specified output directory.

        Args:
            img_url_list (list of Image): List of data of images

        Raises:
            ValueError: If an image URL does not contain a valid image extension.
        """
        # Loop through the requested image URLs and download the images.
        for index, image_url in enumerate(self.image_list[:number_of_images]):
        
            image: Image = image_url
            local_file_name = image.generate_filename(index)

            # Download picture from url.
            try:
                urllib.request.urlretrieve(image.url, os.path.join(
                    self.output_dir, f"{local_file_name}.jpg"))
            except Exception as e:
                # If the initial download fails, try removing any suffixes from the image URL.
                try:
                    img_url = image.url.replace("!Large.jpg", "").replace(
                        "!Large.png", "").replace("!Large.jpeg", "")
                    urllib.request.urlretrieve(img_url, os.path.join(
                        self.output_dir, f"{local_file_name}.jpg"))
                except Exception as e:
                    # If the download still fails, print an error message and move on to the next image.
                    print(f"Error downloading image from URL: {image.url}")
                    print(e)

    def save_image_urls():
        """_summary_
        """


    def load_all_pictures(self):
        """_summary_

        """
        refreshCount = self.count_refresh_actions()
        self.load_more(refreshCount=refreshCount)
