import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from collections import Counter



class Image:
    """
    Represents an image with a URL, name, painter, and associated epochs.
    """

    def __init__(self, url, name = None, painter = None, epochs = []):
        """
        Initializes a new Image object.

        Args:
            url (string): The URL of the image.
            name (string, optional): The name of the image.
            painter (string, optional): The painter of the image.
            epochs (list, optional): A list of epochs associated with the image.
        """
        self.url = url
        self.name = name
        self.painter = painter
        self.epochs = epochs


    def generate_filename(self, index):
        """
        Generates a filename for the image based on its URL and associated epochs.

        Args:
            index (int): The index of the image.

        Returns:
            string: The filename for the image.
        """
        # Set filename from url if possible otherwise use string of i.
        epoch_string = ""
        if self.epochs != None:
            epoch_string = "-".join(self.epochs) + "-"
        
        try:
            # Use regular expressions to extract the filename from the URL.
            reg_results = re.search("images/(.+?)\.jpg", self.url)

            if reg_results == None:
                reg_results = re.search("images/(.+?)\.jpeg", self.url)
 
            if reg_results == None:
                reg_results = re.search("images/(.+?)\.png", self.url)  

            local_file_name = reg_results.group(1)
            local_file_name = local_file_name.replace("/", "_")
            local_file_name = local_file_name.replace("-", ".")
            local_file_name = epoch_string + local_file_name
        except Exception as e:
            # If there is an error with the regex, use the index i as the filename.
            local_file_name = epoch_string + str(index)

        return local_file_name



class WikiartImageScraper:
    """
    Web scraper that uses Selenium and ChromeDriver to extract images from the Wikiart website 
    based on the provided URL and epoch name.
    """

    def __init__(self, url, epoch_name, output_dir, start_index=None, end_index=None):
        """
        Initializes a new WikiartImageScraper object.

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
        informationSections = self.driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
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
        for i in range (0, refreshCount):
            try:
                # The "load more" button may not be found
                self.driver.find_element(By.CLASS_NAME, "masonry-load-more-button").click()
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

        # Go back to the previous page and wait for it to load.
        self.driver.back()
        self.driver.implicitly_wait(30)

        return epoch_list
    

    def get_image_urls(self, painter=None):
        """
        Gets the URLs of the images and the epochs in which they belong.
    
        Returns:
            img_list (list): List of images
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")
        img_list = []
        
        # Set the start and end indices for the range of images to scrape.
        if self.start_index is None:
            self.start_index = 0

        if self.end_index is None:
            self.end_index = len(items)

        print(len(items))
        if len(items) == 20 and painter != None:
            print("Bilder fehlen eventuell bei Maler: "+ str(painter))
            return []

        # Loop through the list of images and extract their URLs and epochs.
        for index in range(self.start_index, self.end_index):
            item = items[index]
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # Scroll to the image and extract its source URL.
                actual_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.execute_script("arguments[0].scrollIntoView();",img_element )
                img_src = img_element.get_attribute("src")

                epoch_list = self.get_epochs(img_element)
                # epoch_list = None

                # Replace the small image URL with the large one and add it to the list.
                img_src = img_src.replace("PinterestSmall", "Large")

                img_list.append(Image(url= img_src, epochs= epoch_list))

        return img_list
    

    def get_painters(self):
        """
        Get the painters of the featured images.
    
        Returns:
            painters_list (list): list of the painters of the featured pictures
        """
        # Find the container that holds all the images.
        html_pictures_list = self.driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
        # Get all the list items that contain the images.
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")
        painters_list = []
        
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

                # Replace the small image URL with the large one and add it to the list.
                img_src = img_src.replace("PinterestSmall", "Large")

                # Extract painter out from url
                painter = self.get_painter_from_url(img_src)
                # append painter name to list
                painters_list.append(painter)

        return painters_list
  

    def painter_counter(self):
        """
        Get the Counter of the painters from the featured painters of the epoch
    
        Returns:
            counter : Counter object of the painters from the featured painters of the epoch
        """

        painter_list = self.get_painters()
        counter = Counter(painter_list)
        return counter
    

    def save_to_file(self, file_name, object): #TODO: könnte erstellen der Datei, wenn nötig, hinzufügen
        """
        Save object as text to file 

        Parameter:
            file_name : name of file to write in
            object: object that should be written as text
        """
        with open(self.output_dir + "/" + file_name, "w") as f:
            f.write(str(object))


    def read_authors_from_file(self, file_name):
        """
        Get list of authors and the count of their featured pictures from file

        Parameter:
            file_name : name of file with counter object of painters

        Returns:
            painter_list (list) : painters named in file
            image_count_list (list)
        """

        with open(self.output_dir + "/" + file_name, "r") as r:
            text = r.read()
            painter_list = re.findall("\'(.+?)\':", text)
            image_count_list = re.findall(": (.+?)[,\}]", text)
            return painter_list, image_count_list
        

    def get_count_of_available_images_from_authors(self,painters_list, epoch):
        """
        Get count of pictures reachable from the painters of epoch

        Parameter:
            painters_list (list) : names of painters
            epoch (String): name of epoch

        Returns:
            image_count : count of reachable images
        """
        image_count = 0

        for index in range(0,len(painters_list)):
            try:
                found_images = 0

                # Get Url of the pictures from the author of the chosen epoch
                self.navigate_to_url("https://www.wikiart.org/en/"+ painters_list[index] +"/all-works#!#filterName:Style_" + epoch + ",resultType:masonry")
                self.driver.implicitly_wait(10)

                # Find the load more button
                informationSections = self.driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
                self.driver.implicitly_wait(5)

                # Check if theres a load more button
                if informationSections[0].text != "":
                    # Read the picture number from the button
                    pictureNumber = int(informationSections.pop().text.split(" ").pop())
                    found_images = pictureNumber
                else:
                    # Count images dispayed on the screen
                    html_pictures_list = self.driver.find_elements(By.CLASS_NAME, "wiki-masonry-container")
                    items = html_pictures_list[0].find_elements(By.TAG_NAME, "li")
                    found_images = 0
                    for item in items:
                        img_elements = item.find_elements(By.TAG_NAME, "img")
                        found_images = found_images + int(len(img_elements))
                
                # Add found images from the author to total count
                image_count = image_count + found_images
            except:
                print("Images of "+ str(painters_list[index]) + " not reachable")

        return image_count
      

    def get_images_from_painters(self, painters_list, epoch):
        """
        Get the URLs of the painters

        Parameter:
            painters_list (list) : names of painters
            epoch (String): name of epoch

        Returns:
             img_list (list): List of images
        """
        img_list = []

        #self.start_index = 20 #TODO: zu testzwecken
        self.end_index = 20 #TODO: zu testzwecken

        if self.start_index == None:
            self.start_index = 0
        
        if self.end_index == None:
            self.end_index = len(painters_list)

        for index in range( self.start_index , self.end_index):
            try:
                img_list = img_list + self.get_images_from_painter(painters_list[index], epoch)
            except:
                print("Images of "+ str(painters_list[index]) + " not reachable")

        return img_list
    

    def get_images_from_painter(self, painter, epoch):
        img_list = []

        # Get Url
        self.navigate_to_url("https://www.wikiart.org/en/" + painter + "/all-works#!#filterName:Style_" + epoch + ",resultType:masonry")
        self.driver.implicitly_wait(40)

        # Find Load More Button
        foo = self.driver.find_elements(by=By.CLASS_NAME, value= "masonry-load-more-button-wrapper")[0]
        elements = foo.find_elements(by= By.CLASS_NAME, value= "masonry-load-more-button")[0]
        link = elements.find_elements(by=By.CLASS_NAME, value="count")[0].text

        # If not all Pictures visible click onto load more button
        if link != "":
            label = self.driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
            self.driver.implicitly_wait(5)
            pictureNumber = int(label.pop().text.split(" ").pop())

            refresh_number = (pictureNumber - 20) / 60
            refresh_number = refresh_number + 1
            refresh_number = int(refresh_number)

            self.load_more(refresh_number)

        self.start_index = None
        self.end_index = None

        img_list = self.get_image_urls(painter)
        
        return img_list


    def download_images(self, number_of_images, img_list):
        """
        Download images from a list of image URLs and saves them to the specified output directory.

        Args:
            img_url_list (list of Image): List of data of images

        Raises:
            ValueError: If an image URL does not contain a valid image extension.
        """
        # Loop through the image URLs and download the images.
        for i in range(len(img_list)):
            # Check if we have already downloaded the maximum number of images.
            if i >= number_of_images:
                pass
            else:
                image : Image = img_list[i]
                local_file_name = image.generate_filename(i)

                # Download picture from url.
                try:
                    urllib.request.urlretrieve(image.url, os.path.join(self.output_dir, f"{local_file_name}.jpg"))
                except Exception as e:
                     # If the initial download fails, try removing any suffixes from the image URL.
                    try:
                        img_url = image.url.replace("!Large.jpg", "").replace("!Large.png", "").replace("!Large.jpeg", "")
                        urllib.request.urlretrieve(img_url, os.path.join(self.output_dir, f"{local_file_name}.jpg"))
                    except Exception as e:
                        # If the download still fails, print an error message and move on to the next image.
                        print(f"Error downloading image from URL: {image.url}")
                        print(e)
                        pass