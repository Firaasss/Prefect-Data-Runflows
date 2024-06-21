import requests, pandas, random, time, re
import psycopg2
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry

##db config
conn = psycopg2.connect(
    database="PriceMyCar",
    user="postgres",
    password="scrubbed",
    host="scrubbed",
    port="scrubbed"
)


def header():

    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    user_agent = random.choice(user_agent_list)

    getHeader = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.kijiji.ca/b-cars-vehicles/ontario/c27l9004',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    return getHeader


    
    try:
        item_info_list = []
        html = urlopen(url)
        bs_item = BeautifulSoup(html, 'html.parser')
        
        try: 
            item_brand = bs_item.find(itemprop='brand').text
        except:
            item_brand = None

        try:
            item_model = bs_item.find(itemprop='model').text
        except:
            item_model = None
        
        try:
            item_date = int(bs_item.find(itemprop='vehicleModelDate').text)
        except:
            item_date = None
        
        try:
            item_price = int(float(bs_item.find('span',itemprop='price').text.replace("\n", "").replace(" ","").replace("$","").replace(",","")))
        except:
            item_price = None
        
        try:
            item_color = bs_item.find(itemprop='color').text
        except:
            item_color = None
            
        try:
            item_config = bs_item.find(itemprop='vehicleConfiguration').text
        except:
            item_config = None
        
        try:
            item_condition = bs_item.find(itemprop='itemCondition').text
        except:
            item_condition = None
        
        try:
            item_bodytype = bs_item.find(itemprop='bodyType').text
        except:
            item_bodytype = None
            
        try:
            item_wheelConfig = bs_item.find(itemprop='driveWheelConfiguration').text
        except:
            item_wheelConfig = None
            
        try:
            item_transmission = bs_item.find(itemprop='vehicleTransmission').text
        except:
            item_transmission = None
            
        try:
            item_fueltype = bs_item.find(itemprop='fuelType').text
        except:
            item_fueltype = None
            
        try:
            item_mileage = int(bs_item.find(itemprop='mileageFromOdometer').text.replace(',', ''))
        except:
            item_mileage = None

        item_carfax = bs_item.find('a', href=re.compile('^(https://reports.carproof.com)((?!:).)*$'))
        try:
            item_carfax_link = item_carfax.attrs['href']
        except:
            item_carfax = bs_item.find('a', href=re.compile('^(https://www.carproof.com)((?!:).)*$'))
            try: 
                item_carfax_link = item_carfax.attrs['href']
            except:
                item_carfax_link = None
        
        try:
            item_dealer_add = bs_item.find(itemprop='address').text
        except:
            item_dealer_add = None

        item_info_list.append(item_brand)
        item_info_list.append(item_model)
        item_info_list.append(item_date)
        item_info_list.append(item_price)
        item_info_list.append(item_color)
        item_info_list.append(item_config)
        item_info_list.append(item_condition)
        item_info_list.append(item_bodytype)
        item_info_list.append(item_wheelConfig)
        item_info_list.append(item_transmission)
        item_info_list.append(item_fueltype)
        item_info_list.append(item_mileage)
        item_info_list.append(item_carfax_link)
        item_info_list.append(item_dealer_add)
    
        
        return item_info_list

    except requests.exceptions.ConnectionError as e:
        return print("ERROR: Can't get page:") 

def scrape(url):
    
    try:
        item_info_list = []
        html = urlopen(url)
        bs_item = BeautifulSoup(html, 'html.parser')
        
        try: 
            item_brand = bs_item.find(itemprop='brand').text
            if item_brand == "Other":
                return 1
        except:
            return 1

        try:
            item_model = bs_item.find(itemprop='model').text
            if item_model == "Other":
                return 1
        except:
            return 1
        
        try:
            item_date = int(bs_item.find(itemprop='vehicleModelDate').text)
            if item_date == "Other":
                return 1
        except:
            return 1
        
        try:
            item_price = int(float(bs_item.find('span',itemprop='price').text.replace("\n", "").replace(" ","").replace("$","").replace(",","")))     
        except:
                return 1
        
        try:
            item_color = bs_item.find(itemprop='color').text
        except:
            item_color = None
            
        try:
            item_config = bs_item.find(itemprop='vehicleConfiguration').text
        except:
            item_config = None
        
        try:
            item_condition = bs_item.find(itemprop='itemCondition').text
        except:
            item_condition = None
        
        try:
            item_bodytype = bs_item.find(itemprop='bodyType').text
        except:
            item_bodytype = None
            
        try:
            item_wheelConfig = bs_item.find(itemprop='driveWheelConfiguration').text
        except:
            item_wheelConfig = None
            
        try:
            item_transmission = bs_item.find(itemprop='vehicleTransmission').text
        except:
            item_transmission = None
            
        try:
            item_fueltype = bs_item.find(itemprop='fuelType').text
        except:
            item_fueltype = None
            
        try:
            item_mileage = int(bs_item.find(itemprop='mileageFromOdometer').text.replace(',', ''))
        except:
            return 1

        item_carfax = bs_item.find('a', href=re.compile('^(https://reports.carproof.com)((?!:).)*$'))
        try:
            item_carfax_link = item_carfax.attrs['href']
        except:
            item_carfax = bs_item.find('a', href=re.compile('^(https://www.carproof.com)((?!:).)*$'))
            try: 
                item_carfax_link = item_carfax.attrs['href']
            except:
                item_carfax_link = None
        
        try:
            item_dealer_add = bs_item.find(itemprop='address').text
        except:
            item_dealer_add = None

        item_info_list.append(item_brand)
        item_info_list.append(item_model)
        item_info_list.append(item_date)
        item_info_list.append(item_price)
        item_info_list.append(item_color)
        item_info_list.append(item_config)
        item_info_list.append(item_condition)
        item_info_list.append(item_bodytype)
        item_info_list.append(item_wheelConfig)
        item_info_list.append(item_transmission)
        item_info_list.append(item_fueltype)
        item_info_list.append(item_mileage)
        item_info_list.append(item_carfax_link)
        item_info_list.append(item_dealer_add)
    
        
        return item_info_list

    except requests.exceptions.ConnectionError as e:
        return print("ERROR: Can't get page:") 

master_list = []
currentCar = []

title=[]
price=[]
itemurl=[]

base_url = 'https://www.kijiji.ca'
init_url = 'https://www.kijiji.ca/b-cars-trucks/ontario/c174l9004'

for page in range(1,150):
    print("***** Fetching PAGE {} ******\n".format(page))
    page_url = 'https://www.kijiji.ca/b-cars-trucks/ontario/'+'page-'+ str(page)+'/c174l9004'
    html = urlopen(page_url)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/v-cars-trucks/)((?!:).)*$')):
        if 'href' in link.attrs:
            item_url = base_url + link.attrs['href']
            if '?' not in item_url:
                print(item_url)
                time.sleep(3)
                currentCar = scrape(item_url) 
                ##if price, make, model, year does not have a value, skip the iteration
                if (currentCar == 1):
                    print("* Skipped invalid iteration *")
                    continue
                else:
                    master_list.append(currentCar)  #master list holding all car data - not erased after each iteration
                    curr = conn.cursor()
                    curr.execute("INSERT INTO cars (brand, model, year, price, color, trim, condition, body_type, wheel_config, transmission, fuel_type, mileage, carfax, address) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", currentCar);
                    conn.commit()
                    print("Successfully added car to database!")
                    
                    currentCar = []  #reinitializing temporary list holding current iteration's car data
conn.close()
df = pandas.DataFrame(master_list)
print(df)
df.to_csv('car_urls.csv')
