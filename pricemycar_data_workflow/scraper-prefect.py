import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from prefect import task, Flow
from prefect.blocks.notifications import SlackWebhook
import re

@task
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

@task
def scrape_me_data(url):
    try:
        html = urlopen(url)
        webpage = BeautifulSoup(html, 'html.parser')

        details_section = webpage.find('ul', class_='cUKQrv')
        details = details_section.find_all('li', class_='crIxcw')

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

@task
def print_car_record(car_record):
    if car_record:
        print(car_record)

@task
def send_slacky():
    slack_webhook_block = SlackWebhook.load("slack-webby")
    slack_webhook_block.notify("Another selection of cars were scraped... happy days!")

@Flow
def car_scraper_flow(url):
    links = url_grabber(url)
    for link in links:
        car_record = scrape_me_data(link)
        print_car_record(car_record)
    ##send a slack notification after all of the records were purged and created.
    send_slacky()

    

if __name__ == "__main__":
    car_scraper_flow("https://www.kijiji.ca/b-cars-trucks/ontario/1c174l9004")
    
