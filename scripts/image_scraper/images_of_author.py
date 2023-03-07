import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def download_images(img_url_list):

    print(f"Anzahl Image Urls in Liste: {len(img_url_list)}")
    print(f"Runterladen bis Bild: {len(img_url_list) - 1}")
    print("Bilddownload gestartet...")

    ############ DOWNLOAD IMAGES FROM URL LIST ############

    for i in range (0, len(img_url_list)):
       
        # set filename from url if possible otherwise use i

        try:
           reg_results = re.search("images/(.+?)\.jpg", img_url_list[i])

           if reg_results == None:
                reg_results = re.search("images/(.+?)\.jpeg", img_url_list[i])

           if reg_results == None:
                reg_results = re.search("images/(.+?)\.png", img_url_list[i])  

           local_file_name = reg_results.group(1)
           local_file_name = local_file_name.replace("/", "_")
           local_file_name = local_file_name.replace("-", ".")
        except:
            local_file_name = str(i)

        # download picture from url
        try:
            urllib.request.urlretrieve(f"{img_url_list[i]}", f"wikiart_image_scraper/data_image_scrape/{local_file_name}.jpg")
        except:
            try:
                img_url = img_url_list[i]
                img_url = img_url.replace("!Large.jpg", "")
                img_url = img_url.replace("!Large.png", "")
                img_url = img_url.replace("!Large.jpeg", "")
                urllib.request.urlretrieve(f"{img_url}", f"wikiart_image_scraper/data_image_scrape/{local_file_name}.jpg")
            except:
                print(img_url)
                pass
    
    print("Bilddownload abgeschlossen!")  

def load_images_of_author_link(driver, img_url_list):
        driver.get("https://www.wikiart.org/en/salvador-dali/all-works#!#filterName:Style_symbolism,resultType:masonry")
        driver.implicitly_wait(5)
        informationSections = driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
        driver.implicitly_wait(5)

        # Wenn nicht alle Bilder angezeigt werden => auf nachladen klicken
        if informationSections[0].text != "":
            print("Load")
            pictureNumber = int(informationSections.pop().text.split(" ").pop())

            clickrate = (pictureNumber - 20) / 60
            clickrate = clickrate + 1
            clickrate = int(clickrate)

            for click in range(0, clickrate):
                driver.find_element(By.CLASS_NAME, "masonry-load-more-button").click()
                time.sleep(3)


        html_pictures_list = driver.find_elements(By.CLASS_NAME, "wiki-masonry-container")
        items = html_pictures_list[0].find_elements(By.TAG_NAME, "li")
            
        for item in items:
            img_elements = item.find_elements(By.TAG_NAME, "img")
            for img in img_elements:
                # scroll actual image into view to load it
                actual_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("arguments[0].scrollIntoView();",img)

                # extract image src code
                img_src = img.get_attribute("src")

                # modify img urls from small size to large size picture url
                img_src = img_src.replace("PinterestSmall", "Large")

                # append large size picture url to list
                img_url_list.append(img_src)
        
        return img_url_list



def run(style):

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    img_url_list= []

    with open("painter/painters_"+style+".txt", "r") as r:
        text = r.read()
        authors = re.findall("\'(.+?)\':", text)
        counts = re.findall(": (.+?)[,\}]", text)

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # set web driver and url
        driver = webdriver.Chrome(options=options)

        for index in range(0,len(authors)-1):
            try:
                img_url_list = load_images_of_author_link("https://www.wikiart.org/en/" + authors[index] + "/all-works#!#filterName:Style_" + style + ",resultType:masonry", img_url_list)
            except:
                print(authors[index])
        
        download_images(img_url_list)

#TODO: must be set for each style
style = "symbolism"
run(style)