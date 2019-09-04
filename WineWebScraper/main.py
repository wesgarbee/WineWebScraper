# A web scraper specifically for wine.com
# Built by Wes Garbee

import os
import time
import random
import urllib.request
import requests
from bs4 import BeautifulSoup as bSoup


page_number = 0
address = "https://www.wine.com/list/wine/red-wine/cabernet-sauvignon/7155-124-139"
req = requests.head(address)
code = req.status_code

address = input("Enter URL: ").strip()

while code is 200:
    address = address + "/" + str(page_number)
    wine_type = address.split("/")[-3]
    print(wine_type)

    dir_name = ("./images/" + wine_type.replace("-", "_").lower())

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    req = requests.get(address)

    soup = bSoup(req.text, "html.parser")
    wines = soup.findAll("li", {"class": "prodItem"})

    for wine in wines:
        wine_text = wine.find("span", {"class": "prodItemInfo_name"}).text
        wine_varietal_text = wine.find("span", {"class": "prodItemInfo_varietal"}).text
        wine_origin = wine.find("span", {"class": "prodItemInfo_originText"}).text
        wine_img_element = wine.find('img')
        wine_img = ("https://www.wine.com/" + wine_img_element.get('src'))
        wine_img_path = ("./" + dir_name + "/" + wine_text.replace(" ", "_") + ".jpg")
        urllib.request.urlretrieve(wine_img, wine_img_path)

        try:
            print(wine_text)
            print(wine_varietal_text)
            print(wine_origin)
            print(wine_img_path)
        except Exception as e:
            print("Error: ", e)

    page_number += 1

    # Sets delay so as not to overload the server
    seconds = random.randrange(90, 120)
    time.sleep(seconds)

    # Gets status code.
    code = requests.head(address).status_code
    if code != 200:
        print("Status code:", code)
