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
            self.log("Webdriver closed.")
        except AttributeError:
            pass

    def log(self, info, noprint=False):
        """
        Prints out the info and saves it in the log_file

        Args:
            info (string): The info which should be printed and logged.
        """
        if not noprint:
            print(info)

        log_file_path = os.path.join(self.output_dir, "log.txt")
        with open(log_file_path, 'a') as log_file:
            log_file.write(info + "\n")
    
    def print_progress_bar(self, amount, of, start_text = "Progress", end_text = "", new_line = True):
        progress = int(((amount)/of)*100)
        progress_bar = f"{start_text}: [{'='*int(progress/2)}{' '*(50-int(progress/2))}] {progress}% ({amount}/{of}) {end_text}"
        print(progress_bar, end="\r" if not new_line and progress < 100 else "\n")

    def remove_image_duplicates(self):
        """
        Removes duplicates in the image_list.
        """
        self.log(f"Removed image duplicates of {self.epoch_name}")
        self.image_list = list(set(self.image_list))

    def start_driver(self):
        """
        Initializes and start the Chrome webdriver with the provided options and
        navigate to the URL provided during the initialization of the class.
        """
        self.driver = webdriver.Chrome(options=self.options)
        self.navigate_to_url(self.url)
        self.log("Webdriver started...")
        time.sleep(3)
    

    def navigate_to_url(self, url):
        """
        Navigate the webdriver to the specified URL.

        Args:
            url (string): The URL to navigate to.
        """
        self.driver.get(url)


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
        refreshCount = refreshCount - 1

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
            self.print_progress_bar(i+1, refreshCount, start_text ="Load more", new_line = False)


    def load_all_images(self):
        """
        Refreshes the page and scrolls to show all images.

        """
        refreshCount = self.count_refresh_actions()
        self.load_more(refreshCount=refreshCount)
    

    def get_painters(self):
        """
        Get the painters of the featured images.
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(
            By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")

        # Loop through the list of images and extract their URLs and epochs.
        for index, item in enumerate(items):
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
            self.print_progress_bar(index+1, len(items), start_text="Scanned images for painters", new_line = False)


    def get_painter_from_url(self, img_src):
        """
        Gets the painter of an image.

        Args:
            img_src (string): String representing the image path.

        Returns:
            string: Name of the painter of the image.
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


    def get_important_painters_of_epoch(self):
        """
        Get the important painters of epoch via epoch painters overview site.
        """
        # Handle differnet naming of art-nouveau-modern
        epoch = self.epoch_name
        if self.epoch_name == "art-nouveau-modern":
            epoch = "art-nouveau"

        try:
            self.navigate_to_url(f"https://www.wikiart.org/en/artists-by-art-movement/{epoch}#!#resultType:masonry")
            self.driver.implicitly_wait(30)
        except:
            self.log(f"URL of important painters of {epoch} not found.")

        self.get_painters_of_overview()

    def get_painters_of_overview(self, epoch_name):
        """
        Get the list of painters from an overview site.

        Parameter:
            epoch_name : name of epoch
        """

        calculated = False

        while not calculated:
            try:
                self.driver.implicitly_wait(5)
                informationSections = self.driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
                self.driver.implicitly_wait(5)
                pictureCount = int(informationSections.pop().text.split(" ").pop())
                calculated = True
            except:
                time.sleep(2)

        # Divide the total number of pictures by 60, which is the default number of pictures loaded per page.
        refreshCount = int(pictureCount/60)

        self.load_more(refreshCount=refreshCount)

        try: 
            # Find the container that holds all the images.
            html_pictures_list = self.driver.find_elements(
                By.CLASS_NAME, "wiki-artistgallery-container.ng-isolate-scope")
            # Get all the list items that contain the images.
            items = html_pictures_list[0].find_elements(By.TAG_NAME, "li")

            # Loop through the list of images and extract their URLs and epochs.
            for index, item in enumerate(items):
                img_elements = item.find_elements(By.CLASS_NAME, "image-wrapper")
                for img_element in img_elements:
                    # Scroll to the image and extract its source URL.
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView();", img_element)
                    href = img_element.get_attribute("href")

                    # Extract painter out from href
                    painter = href.split("/")[4]

                    if painter in self.painters_dict:
                        self.painters_dict[painter] += 1
                    else:
                        self.painters_dict[painter] = 1
                self.print_progress_bar(index+1, len(items),start_text="Scanned epoch painters", new_line=False)
        except:
            self.log(f"Finding painters of epoch {epoch} failed.")
            return

    def get_images_from_painters(self, startIndex = 0, endIndex = None):
        """
        Get the image objects of the pictures of the painters in range from start to end index.

        Parameter:
            startIndex : index of first used painter
            endIndex : index of last used painter
        """
        if endIndex == None:
            endIndex = len(self.painters_dict)
        self.log(f"Get images of {endIndex-startIndex} painters ({startIndex}-{endIndex-1})")
        for index, painter in enumerate(dict(list(self.painters_dict.items())[startIndex:endIndex+1])):
            try:
                self.image_list += self.get_images_from_painter(painter=painter)
            except:
                self.log(f"Error by getting images from {painter}")
            self.log(f"Finished painter {painter} ({index})", noprint=True)
            self.print_progress_bar(index+1, endIndex-startIndex, start_text="Get images from painters", end_text = f"Finished {painter}")


    def get_images_from_painter(self, painter):
        """
        Get the image objects of the pictures of the painter.

        Args:
            painter (string): The painter of the image.

        Returns:
            list of images: List containing the image objects.
        """
        if not self.is_painter_available(painter=painter):
            return []
        
        try:
            # Get Url
            self.navigate_to_url("https://www.wikiart.org/en/" + painter + "/all-works#!#filterName:Style_" + self.epoch_name + ",resultType:masonry")
            self.driver.implicitly_wait(40)
        except:
            self.log(f"Cant find URL of {painter}.")
            return []
        
        #Check if not all images of painter are shown and not only the epoch ones
        #That might happen if an wrong painter is in the list
        try:
            subtitles = self.driver.find_elements(by=By.CLASS_NAME, value="subtitle.ng-binding.ng-scope")
            text = subtitles[0].text
            if self.epoch_name not in text.lower():
                print(f"Might show all images of painter {painter}")
                return
        except:
            print(f"Error acessing subtitle: {painter}")
            return
        
        try:
            # Find Load More Button
            load_more_button = self.driver.find_elements(
                by=By.CLASS_NAME, value="masonry-load-more-button")[0]
            rawCountText = load_more_button.find_elements(
                by=By.CLASS_NAME, value="count")[0].text
            
            self.driver.implicitly_wait(5)

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
            self.log(f"Images of painter {painter} not reachable.")
            return []

        return self.get_image_list(painter=painter)


    def get_image_list(self, painter=None):
        """
        Gets the URLs of the images and the epochs in which they belong.

        Args:
            painter (string, optional): Name of the painter if driver is on a painter site. 

        Returns:
            img_list (list): List of image urls.
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(
            By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")
        img_list = []

        self.log(f"{len(items)} images from {painter} found.")
        
        # A count of 20 images found can indicate that load more button was not found, painter must be checked manually
        if len(items) == 20 and painter != None:
            self.log("Not all images may be available: " + str(painter))
            return []

        # Loop through the list of images and extract their URLs and epochs.
        for index, item in enumerate(items):
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # Scroll to the image and extract its source URL.
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", img_element)
                img_src = img_element.get_attribute("src")
                try:
                    epochs = self.get_epochs(img_element)
                    if epochs != None:
                        epoch_list = epochs
                    else:
                        print(f"No chosen epochs found for image {img_src}. Not added to list")
                        continue
                except:
                    self.log(f"Could't get the image of soure: {img_src}")
                    epoch_list = [self.epoch_name]
                # Replace the small image URL with the large one and add it to the list.
                img_src = img_src.replace("PinterestSmall", "Large")

                # Appends the created Image to the img list
                img_list.append(Image(url=img_src, epochs=epoch_list))
            self.print_progress_bar(index+1, len(items), start_text="Images found: ", new_line=False)

        return img_list


    def get_epochs(self, img_element):
        """
        Gets the epochs of an image element.

        Args:
            img_element (object): The HTML element of the image.

        Returns:
            list of strings: Epochs of the image.
        """
        epoch_list = []
        self.driver.implicitly_wait(10)

        # Click on the image to open it and extract the epoch information.
        protected = True
        while protected:
            try:
                img_element.click()
                self.driver.implicitly_wait(10)
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
                epoch_name = ""
                # Because of python 3.8
                switch = {
                    "Realism": "realism",
                    "Impressionism": "impressionism",
                    "Romanticism": "romanticism",
                    "Expressionism": "expressionism",
                    "Post-Impressionism": "post-impressionism",
                    "Baroque": "baroque",
                    "Art Nouveau (Modern)": "art-nouveau-modern",
                    "Surrealism": "surrealism",
                    "Symbolism": "symbolism"
                }
                epoch_name = switch.get(epoch.text)
                if epoch_name != None:
                    epoch_list.append(epoch_name)
                else:
                    return None

            # Last element gets removed because it isn't an epoch
            # epoch_list.remove(epoch_list[len(epoch_list)-1])
        except:
            self.log(f"Epochs not found")
            epoch_list.append(self.epoch_name)

        # Go back to the previous page and wait for it to load.
        self.driver.back()
        self.driver.implicitly_wait(30)

        return epoch_list


    def is_painter_available(self, painter):
        """
        Check if pictures of the painter are available and not restricted.

        Args:
            painter (string): Painter of the image.

        Returns:
            boolean: Boolean indicating the availability of the images.
        """
        try:
            # Get Url
            self.navigate_to_url(f"https://www.wikiart.org/en/{painter}")
            self.driver.implicitly_wait(1)
        except:
            self.log(f"Cant find page of {painter}.")
            return  False
        
        privacy_hint = self.driver.find_elements(by=By.CLASS_NAME, value="wiki-layout-restricted-msg-wrapper")

        if len(privacy_hint) > 0:
            return False

        return True
    

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
                    self.log(f"Error downloading image from URL: {image.url}")
                    self.log(e)


    def save_to_file(self, file_name, dict):
        """
        Save objects in a json file.

        Args:
            file_name (string): The name of file to write in.
            dict (object): The object that should be written as JSON.
        """
        with open(os.path.join(self.output_dir, file_name), "w") as f:
            json.dump(dict, f)


    def save_painters(self):
        """
        Saves the painters_dict of an instance to a json file called "painters.json".
        """
        self.save_to_file("painters.json", self.painters_dict)
        self.log(f"Saved painters of epoch {self.epoch_name}")


    def save_images(self):
        """
        Saves the image_list of an instance to a json file called "images.json".
        """
        json_image_list = []

        for image in self.image_list:
            image_data = {
                "url": image.url,
                "epochs": image.epochs
            }

            json_image_list.append(image_data)

        self.save_to_file("images.json", json_image_list)


    def read_images_from_json(self, file_name):
        """
        Get list of images from json file and write it to the image_list attribute of the class.

        Args:
            file_name (string): Name of the file.
        """
        with open(os.path.join(self.output_dir, file_name), "r") as file:
            json_image_list = json.load(file)
        
        self.image_list = []

        for image in json_image_list:
            image_object = Image(url=image["url"], epochs=image["epochs"])
            self.image_list.append(image_object)

    
    def read_painters_from_json(self, file_name):
        """
        Get list of painters and write it to the painters_dict attribute of the class.

        Args:
            file_name (string): Name of the file.
        """

        with open(os.path.join(self.output_dir, file_name), "r") as file:
            painters_dict = json.load(file)
        
        self.painters_dict = painters_dict


    ##### Not part of ImageScraper pipeline #####
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
                self.log("Images of " +
                    str(painter) + " not reachable")

        return total_image_count
    
    
    def get_search_found_painters_of_epoch(self):
        """
        Get the important painters of epoch via epoch painters overview site.
        Works only for surrealism
        """
        
        if self.epoch_name == "surrealism":
            try:
                self.navigate_to_url(f"https://www.wikiart.org/en/artistadvancedsearch#!#filter:advanced,minYear:-50000,maxYear:2023,dictionaries:57726a67edc2ca38801d4e11")
                self.driver.implicitly_wait(30)
            except:
                print(f"URL of important painters of {self.epoch_name} not found.")

            self.get_painters_of_overview(self.epoch_name)


    def get_won_painters(self, painter_file_name, save_file_name):
        """
        Get painters from file which are not in painters_dict and save them

        Args:
            painter_file_name (string): Name of the file with more painters
            save_file_name (string): Name of file to save the result in
        """

        # Read painters from file
        with open(os.path.join(self.output_dir, painter_file_name), "r") as file:
            painters_dict = json.load(file)
        
        new_painter = {}
        
        # Check for each painter if he is in painters_dict, if not add to new dictionary
        for painter in painters_dict:

            if painter not in self.painters_dict:
                if painter in new_painter:
                    new_painter[painter] += 1
                else:
                    new_painter[painter] = 1

        # Save missing painters to file
        self.save_to_file(save_file_name, new_painter)


    def clear_images(self):
        """
        Clear list of images so they only contain images from selected epoch
        """

        new_list = []

        for img in self.image_list:
            image : Image = img

            append = False
            for epoch in image.epochs:
                if epoch == self.epoch_name:
                    append = True

            if append:
                new_list.append(img)

        self.image_list = new_list
    

    def remove_images_of_painter(self, painter_name):
        """
        Remove images from painter

        Parameter:
            painter_name (string): name of painter
        """
        new_list = []

        for img in self.image_list:
            image : Image = img
            if painter_name not in image.url:
                new_list.append(img)

        self.image_list = new_list
            

    def get_painters_of_all_centuries(self):
        """
        Get all painters form the 15th to 21th century and save them
        """

        for index in range(15,21):

            print(f"Get url of century {index}")
            self.navigate_to_url(f"https://www.wikiart.org/en/artists-by-century/{index}#!#resultType:masonry")
            self.driver.implicitly_wait(30)

            print(f"Find painters of century {index}")
            self.get_painters_of_overview(epoch_name="foo")
        
        self.save_painters()
    

    def filter_painter_of_epoch(self, startIndex = 0, endIndex = None):
        """
        Select from list of painters, which have made images from epoch

        Parameters:
            startIndex : index to start selecting
            endIndex : index to stop selecting
        """
        painter_selected = {}

        if endIndex == None:
            endIndex = len(self.painters_dict)

        # Go through all painters
        for painter in dict(list(self.painters_dict.items())[startIndex:endIndex+1]):

            # Get URL
            try:
                self.navigate_to_url("https://www.wikiart.org/en/" +
                                    painter + "/all-works#!#filterName:Style_" + self.epoch_name + ",resultType:masonry")
                self.driver.implicitly_wait(10)
            except:
                print(f"Error with url:{painter}")
                continue
            
            # Check the subtitle
            try:
                subtitles = self.driver.find_elements(by=By.CLASS_NAME, value="subtitle.ng-binding.ng-scope")
                text = subtitles[0].text

                # Check if painter has images of epoch than add to dictionary
                if self.epoch_name in text.lower():
                    if painter in painter_selected:
                        painter_selected[painter] += 1
                    else:
                        painter_selected[painter] = 1
            except:
                print(f"Error acessing subtitle: {painter}")
                continue

        self.painters_dict = painter_selected
