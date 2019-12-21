import requests
import urllib.request
from bs4 import BeautifulSoup
import re


def scrape_website(html):
    soup = BeautifulSoup(html, 'html.parser')

    allProps = []
    for detail in soup.findAll("div", class_="property__inner"): 
        post_Number = detail.find('div', class_='property__postalcode').text

        street_Address = detail.find('div', class_='property__title').h2.text

        price = detail.find('div', class_='property__price').text
        price = price[:-4]
        price = re.sub(r'\.', '', price)

        image = detail.find('div', class_='property__image').a.img['src']

        id = detail.find('div', class_='property__title').h2.a
        id = str(id)
        id = id.split('/')[2].split('?')[0]

        link = 'http://fasteignir.visir.is/property/' + id

        squareMeter = detail.find('span', class_='property__size').text
        squareMeter = squareMeter[:-5]
        squareMeter = re.sub(r'\,', '.', squareMeter)

        rooms = detail.find('span', class_='property__arrangement').text
        try:
            squareMeterPrice = float(price) / float(squareMeter)
        except:
            continue
        prop = {
            "id" : id,
            "link" : link,
            "post_number" : post_Number,
            "street_Address" : street_Address,
            "rooms": rooms,
            "price" : float(price),
            "squaremeter": float(squareMeter),
            "squareMeter_price": squareMeterPrice,
            "image": image
        }
        allProps.append(prop)
    return allProps

#res = requests.get('http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale').text
#print(scrape_website(res))