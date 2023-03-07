###########################################################################################
####        python script to download the pictures from wikiart automatically        ######
###########################################################################################

import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import Counter

# start selenium web driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def download_wikiart_pics(url, epoch_name, start_index, end_index):
    img_url_list = []
    img_epoch_list = []
    img_data = []

    try:
        # set web driver and url
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        print("Webdriver gestartet...")

        time.sleep(3)

        # find count of nessasary refresh actions
        informationSections = driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
        driver.implicitly_wait(50)
        pictureNumber = int(informationSections.pop().text.split(" ").pop())

        refreshNumber = int(pictureNumber/60)

        #if((pictureNumber % 60)!= 0):
        #    refreshNumber = refreshNumber +1

        refreshNumber = refreshNumber - 2
        print(refreshNumber)

        #refreshNumber = 5   #TODO: Remove for using

        # click load more button
        for i in range (0, refreshNumber):
            try:
                driver.find_element(By.CLASS_NAME, "masonry-load-more-button").click()
            except:
                driver.implicitly_wait(5)
                buttons = driver.find_elements(By.TAG_NAME, "button")
                buttons[0].click()
                i = i-1   
            time.sleep(5)

        print("Click done")

        ############ WRITE IMAGE URLS IN LIST ############

        # extract list with image elements from html
        html_pictures_list = driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")

        if start_index == None:
            start_index = 0

        if end_index == None:
            end_index = len(items)

        print("Write to list")

        for index in range(start_index, end_index):
            item = items[index]
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # scroll actual image into view to load it
                actual_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("arguments[0].scrollIntoView();",img_element )

                # extract image src code
                img_src = img_element.get_attribute("src")


                # modify img urls from small size to large size picture url
                img_src = img_src.replace("PinterestSmall", "Large")

                match = ""
                try:
                    match = re.search("images/(.+?)/", img_src)[0]
                    match = match.split("/")[1]
                except:
                    match = "foo"

                # append large size picture url to list
                img_url_list.append(match)
    except:
        print("Abbruch")
    
    print(f"Anzahl Image Urls in Liste: {len(img_url_list)}")

    if start_index == None :
        print(f"Runterladen bis Bild: {len(img_url_list) - 1}")
    else:
        print(f"Runterladen bis Bild: {start_index + len(img_url_list) - 1}")

    print("Bilddownload gestartet...")

    #print(Counter(img_url_list))
    counter = Counter(img_url_list)

    with open("painters.txt", "w") as f:
        f.write(str(counter))

    #for links in img_url_list:
    #    print(links)

    ############ DOWNLOAD IMAGES FROM URL LIST ############

    #for i in range (0, len(img_url_list)):
       
        # set filename from url if possible otherwise use i
    #    epochs = img_epoch_list[i]
    #    epoch_String = ""
    #    for epoch in epochs:
    #        epoch_String = epoch_String + epoch + "-"

    #    img_data_string = ""
    #    img_data_string = img_data[i]

    #    local_file_name = epoch_String + img_data_string

    #    print(local_file_name)

    
    print("Bilddownload abgeschlossen!")    

#Optional as Int to download parts of the pictures
start_index = None
end_index = None

#TODO: Set before use
#epoch_pictures_link = "https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/en/paintings-by-style/symbolism?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/en/paintings-by-style/surrealism?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/art-nouveau-modern?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/barock?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/post-impressionismus?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/romantik?select=featured#!#filterName:featured,viewType:masonry"
#epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/impressionismus?select=featured#!#filterName:featured,viewType:masonry"
epoch_pictures_link = "https://www.wikiart.org/de/paintings-by-style/realismus?select=featured#!#filterName:featured,viewType:masonry"
epoch_name = "Expressionism"

download_wikiart_pics(epoch_pictures_link, epoch_name, start_index, end_index)