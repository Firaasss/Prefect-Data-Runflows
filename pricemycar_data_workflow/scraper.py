import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def url_grabber(url):
    base_url = 'https://www.kijiji.ca'
    link_urls = []
    
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    
    for link in bs.find_all('a', href=re.compile('^(/v-cars-trucks/)((?!:).)*$')):
        if 'href' in link.attrs:
            item_url = base_url + link.attrs['href']
            link_urls.append(item_url)
        else:
            raise ValueError(f"Could not retrieve link: {link}")

    return link_urls

def scrape_me_data(url):
    try:
        html = urlopen(url)
        webpage = BeautifulSoup(html, 'html.parser')

        details_section = webpage.find('ul', class_='cUKQrv') #cUKQrv grabs the div section containing all the car detail elements
        details = details_section.find_all('li', class_='crIxcw') #crIxcw is the li class denoting each individual detail for the cars

        try:
            item_price = int(float(webpage.find('span', itemprop='price').text.strip().replace("$", "").replace(",", "")))
        except AttributeError:
            item_price = None

        car_details = {}
        for detail in details:
            key = detail.find('span', class_='kTqYUw').text.strip().replace(":", "")
            value = detail.find('span', class_='gfuBsJ').text.strip()
            car_details[key] = value

        try:
            mileage_section = webpage.find('span', class_='sc-gvZAcH dIqqkf', string='Kilometers')
            item_mileage = mileage_section.find_next('span', class_='sc-kRRyDe ifrqid').text.strip()
        except AttributeError:
            item_mileage = None

        car_record = {
            'price': item_price,
            'year': car_details.get('Year', None),
            'make': car_details.get('Make', None),
            'model': car_details.get('Model', None),
            'mileage': item_mileage
        }

        return car_record
    except Exception as e:
        print(f"Skipping {url}: {e}")
        return None

if __name__ == "__main__":
    print("Grabbing a list of links.. one moment please:")
    print()

    links = url_grabber("https://www.kijiji.ca/b-cars-trucks/ontario/1c174l9004")
    print(f"Found {len(links)} links.")

    print("\nLet's extract individual car records..")
    for url in links:
        car_record = scrape_me_data(url)
        if car_record:
            print(car_record)
