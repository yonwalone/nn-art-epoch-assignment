###########################################################################################
####        python script to download the pictures from wikiart automatically        ######
###########################################################################################

import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import Counter

# Zur Weiterarbeit:
# https://vijayabhaskar96.medium.com/multi-label-image-classification-tutorial-with-keras-imagedatagenerator-cd541f8eaf24

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

        if((pictureNumber % 60)!= 0):
            refreshNumber = refreshNumber + 1

        refreshNumber = 1   #TODO: Remove for using

        # click load more button
        for i in range (0, refreshNumber):
            driver.find_element(By.CLASS_NAME, "masonry-load-more-button").click()
            time.sleep(3)

        ############ WRITE IMAGE URLS IN LIST ############

        # extract list with image elements from html
        html_pictures_list = driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
        items = html_pictures_list.find_elements(By.TAG_NAME, "li")

        if start_index == None:
            start_index = 0

        if end_index == None:
            end_index = len(items) - 1

        for index in range(start_index, end_index):
            item = items[index]
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img_element in img_elements:
                # scroll actual image into view to load it
                actual_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("arguments[0].scrollIntoView();",img_element )

                # extract image src code
                #img_src = img_element.get_attribute("src")

                #read epochs from detailspage
                epoch_list = []

                driver.implicitly_wait(20)
                img_element.click()
                driver.implicitly_wait(20)

                #informationSections = driver.find_elements(by=By.CLASS_NAME, value="dictionary-values")
                #if len(informationSections) != 0 :
                #    information = informationSections[0]
                #    epochs = information.find_elements(by=By.TAG_NAME, value="a")
                #    for epoch in epochs:
                        #TODO: Check if epoch is one of our chosen epochs (Switch Case)
                #        epoch_list.append(epoch.text)
                #    epoch_list.remove(epoch_list[len(epoch_list)-1])
                #else:
                #    epoch_list.append(epoch_name)
                #img_epoch_list.append(epoch_list)

                info_string = ""
                #titles = driver.find_elements(by=By.TAG_NAME, value="h3")
                #info_string = info_string + titles[1].text + "_"

                articles = driver.find_elements(by=By.TAG_NAME, value="article")
                article = articles[0]

                dates = article.find_elements(by=By.TAG_NAME, value="span")
                info_string = info_string + dates[0].text + "_"             #Painter
                #info_string = info_string + dates[1].text                   #Year

                #for painter in dates:
                #     info_string = info_string + painter.text + "-"
                
                img_data.append(info_string)  

                driver.back()
                driver.implicitly_wait(30)

                # modify img urls from small size to large size picture url
                #img_src = img_src.replace("PinterestSmall", "Large")

                # append large size picture url to list
                #img_url_list.append(img_src)

    except:
        print("Abbruch")
    
    print(f"Anzahl Image Urls in Liste: {len(img_url_list)}")

    if start_index == None :
        print(f"Runterladen bis Bild: {len(img_url_list) - 1}")
    else:
        print(f"Runterladen bis Bild: {start_index + len(img_url_list) - 1}")

    print("Bilddownload gestartet...")

    print(Counter(img_data))

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
epoch_pictures_link = "https://www.wikiart.org/en/paintings-by-style/expressionism?select=featured#!#filterName:featured,viewType:masonry"
epoch_name = "Expressionism"

download_wikiart_pics(epoch_pictures_link, epoch_name, start_index, end_index)