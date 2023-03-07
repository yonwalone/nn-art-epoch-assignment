import urllib.request
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def run():
    potential = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])


    with open("painter/painters_post-impressionism.txt", "r") as r:
        text = r.read()
        authors = re.findall("\'(.+?)\':", text)
        counts = re.findall(": (.+?)[,\}]", text)

        style = "post-impressionism"

        print(authors)
        print(authors[1])
        print(len(authors))
        print(counts[0])
        print(len(counts))

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # set web driver and url
        driver = webdriver.Chrome(options=options)

        # For-Schleife

        for index in range(0,len(authors)):
            try:
                win = 0
                driver.get("https://www.wikiart.org/en/"+ authors[index] +"/all-works#!#filterName:Style_" + style + ",resultType:masonry")
                driver.implicitly_wait(5)
                informationSections = driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
                driver.implicitly_wait(5)
                if informationSections[0].text != "":
                    pictureNumber = int(informationSections.pop().text.split(" ").pop())
                    win = pictureNumber
                    #win = pictureNumber - int(counts[index])
                else:
                    #print("Else")
                    html_pictures_list = driver.find_elements(By.CLASS_NAME, "wiki-masonry-container")
                    #print(len(html_pictures_list))
                    items = html_pictures_list[0].find_elements(By.TAG_NAME, "li")
                    win = 0
                    for item in items:
                        img_elements = item.find_elements(By.TAG_NAME, "img")
                        win = win + int(len(img_elements))
                    #print(win)
                    #win = win - int(counts[index])

                potential = potential + win
                print(potential)
            except:
                print(authors[index])

    return
    # set web driver and url
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.wikiart.org/en/"+ "bela-czobel" +"/all-works#!#filterName:Style_expressionism,resultType:masonry")
    driver.implicitly_wait(10)
    informationSections = driver.find_elements(by=By.CLASS_NAME, value="count.ng-binding")
    driver.implicitly_wait(10)
    print("Hallo")
    win = 0
    html_pictures_list = driver.find_element(By.CLASS_NAME, "wiki-masonry-container")
    items = html_pictures_list.find_elements(By.TAG_NAME, "li")
    for item in items:
        img_elements = item.find_elements(By.TAG_NAME, "img")
        win = win + len(img_elements)
    print(win)




run()