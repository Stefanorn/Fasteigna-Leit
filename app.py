import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import json
import pymongo
import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
import time
from Create_Email_Content import Create_Email_Content
from Constnts import Constnts

### TODO ætti að breyta þessu í margar skrár
### TODO það þirfti að laga öll breytunöfn hafa samræmi þetta er sick


## TODO þarf að gera enviroment breytur


class User(object):
    def __init__(self, email, min_price, max_price, min_rooms, zip_codes, best_search_pricecutof):
        self.email = email
        self.min_price = min_price
        self.max_price = max_price
        self.min_rooms = min_rooms
        self.zip_codes = zip_codes
        self.best_search_pricecutof = best_search_pricecutof
    def getUsername(self):
        #TODO láta þetta skil emailinu - email eða eitthvað
        username = re.sub(r'@.+', '', self.email)
        username = re.sub(r'\.', '', username)
        return username


##################################################################
#  Data_gathering fuctions
##################################################################
def scrape_website(html):
    soup = BeautifulSoup(html, 'html.parser')

    allProps = []
    for detail in soup.findAll("div", class_="property__details"): 
        post_Number = detail.find('div', class_='property__postalcode').text

        street_Address = detail.find('div', class_='property__title').h2.text

        price = detail.find('div', class_='property__price').text
        price = price[:-4]
        price = re.sub(r'\.', '', price)

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
            "image": "https://i.imgur.com/OWLoorP.jpg"
        }
        allProps.append(prop)
    return allProps

##################################################################
#  Data_manipulation_functions
##################################################################
### TODO breyta þessu i klasa
def sort_by_price( item ):
    return item['price']
def sort_by_sqaremeter(item):
    return item['squaremeter']
def sort_by_sqaremeter_price(item):
    return item['squareMeter_price']
def find_lowest_prices( data, index):
    data.sort(key=sort_by_price)
    return data[:index]
def find_cheepes_squaremeter( data, index ):
    data.sort(key=sort_by_sqaremeter_price)
    return data[:index]
def find_avrage_price(data):
    totalSum = 0
    for item in data:
        totalSum = totalSum + item['price']
    if totalSum == 0:
        return -1
    if len(data) == 0:
        return -1
    return totalSum / len(data)
def find_avrage_squaremeter_price(data):
    totalSum = 0
    for item in data:
        totalSum = totalSum + item['squareMeter_price']
    return totalSum / len(data)

def find_biggest_propertys(data,index):
    data.sort(key=sort_by_sqaremeter,reverse=True)
    return data[:index]

def find_Best_Priced(data, scope_amount):
    i = 0
    scope_index = int(len(data) / 10)
    if(scope_index < 5 ):
        scope_index = 5
    intresting_appartments = [{}]
    intresting_appartments.pop()

    data.sort(key=sort_by_sqaremeter,reverse=True)
    while i < len(data) - scope_index-1:
        avg = find_avrage_squaremeter_price(data[i:scope_index+i])
        if( data[i+scope_index+1]['squareMeter_price'] - avg < -scope_amount):
            data[i+scope_index+1]['Price Below Avrage'] = data[i+scope_index+1]['squareMeter_price'] - avg
            intresting_appartments.append(data[i+scope_index+1])
        i += 1
    ## todo ath þetta fall skippar fyrstu 5 (scope_index) fasteignum þarf að búa til loopu sem skoðar þær
    return intresting_appartments

##################################################################
#  Data_gathering exporting
##################################################################
def add_row_to_database(table_row, connection_string, database, collection ):
    mng_client = pymongo.MongoClient(connection_string)
    mng_db = mng_client[database]
    db_cm = mng_db[collection]
    db_cm.insert_one(table_row)

def Get_rows_from_today(connection_string, database, collection):
    
    today = datetime.today()
    start = datetime(today.year, today.month, today.day, 0, 0)
    end = datetime(today.year, today.month, today.day, 23, 59)

    mng_client = pymongo.MongoClient(connection_string)
    mng_db = mng_client[database]
    db_cm = mng_db[collection]
    ret = list(db_cm.find({ "time": {'$lt': end, '$gte': start}}))
    return ret

def print_to_console(data):
    print(generate_generic_text(data))
def generate_generic_text(data):
    retString = ''
    retString += data['City'] + '\n'
    retString += 'Meðalverð : ' + str(int(data['avrage price'])) + ' kr' + '\n'
    retString += '\n'
    retString += 'Fann ' + str(len(data['best priced'])) + ' íbúðir :' + '\n'
    retString += '------------------------------' + '\n'
    for item in data['best priced']:
        retString += item['street_Address'] + ', ' + item['rooms'] + '\n'
        retString += 'Verð - ' + str(int(item['price'])) + ' kr, stærð - ' + str(int(item['squaremeter'])) + ' m2' + '\n'
        retString += 'Fermetraverð : ' + str(int(item['squareMeter_price'])) + ' kr/m2' + '\n'
        retString += 'hlekkur : '  + item['link']  + '\n'
        retString += '\n'
    retString += '------------------------------' + '\n'
    retString += 'Leitarskilyrði' + '\n'
    retString += 'verðbil : ' + str(int(data['search term price'][0])) + " til " + str(int(data['search term price'][1])) + " kr" + '\n'
    retString += 'herbergi : ' + str(int(data['search term min rooms'])) + '\n'
    return retString
def send_email(content, email, zip_code):
    EMAIL_ADDRESS = Constnts.EMAIL_ADDRESS
    EMAIL_PASSWORD = Constnts.EMAIL_PASSWORD
    msg = EmailMessage()
    msg['Subject'] = 'Áhugaverdar íbúðir í ' + zip_code 
    msg['From'] = 'ekkisvara69@gmail.com'
    msg['To'] = email
    msg.set_content( content )

    msg.add_alternative(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

def get_data_from_site( min_price, max_price, min_rooms, zip_code):
    site_request = [
        'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip='+ str(zip_code) +'&category=1,2,4,7&price=' + str(min_price) +',' + str(max_price) + '&room='+str(min_rooms)+',10&itemcount=60&page=1',
        'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip='+ str(zip_code) +'&category=1,2,4,7&price=' + str(min_price) +',' + str(max_price) + '&room='+str(min_rooms)+',10&itemcount=60&page=2',
        'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip='+ str(zip_code) +'&category=1,2,4,7&price=' + str(min_price) +',' + str(max_price) + '&room='+str(min_rooms)+',10&itemcount=60&page=3',
        'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip='+ str(zip_code) +'&category=1,2,4,7&price=' + str(min_price) +',' + str(max_price) + '&room='+str(min_rooms)+',10&itemcount=60&page=4',
        'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip='+ str(zip_code) +'&category=1,2,4,7&price=' + str(min_price) +',' + str(max_price) + '&room='+str(min_rooms)+',10&itemcount=60&page=5'
    ]
    site_data = []
    for req in site_request:
        res = requests.get(req).text
        data = scrape_website(res)
        if len(data) == 0:
            break
        site_data = site_data + data
        ## TODO Sleepa hér til að vera ekki að spamma visir.is
        time.sleep(1)
    return site_data

start_time = time.time()
print( str(datetime.today()) + ' Start')


user_list = []
user_list.append(User('stefanorn92@gmail.com',1000000,50000000,3,['221','220','200','201','203','240'],15000))
user_list.append(User('martamagnusd@live.com',1000000,50000000,3,['221','220'],15000))
user_list.append(User('vidir17@ru.is',1000000,50000000,1,['109','112','113','200','201','203','210','212','225','220','221','222'],15000))

for user in user_list:
    content = Create_Email_Content()
    content_was_added = False
    for zip_code in user.zip_codes:
        username = user.getUsername()
        today_rows = Get_rows_from_today(Constnts.DB_CONNECTION_STRING, username, zip_code)
        if len(today_rows) >= 1:
            db_items = today_rows[0]['best priced']
            site_data = get_data_from_site( user.min_price, user.max_price, user.min_rooms, zip_code )
            if len(site_data) == 0:
                continue
            site_items = find_Best_Priced(site_data, user.best_search_pricecutof)
            ## TODO ójj?? 
            db_items_id = []
            for item in db_items:
                db_items_id.append(item['id'])
            not_same = []
            for i in range(0,len( site_items ),1):
                if site_items[i]['id'] not in db_items_id:
                    not_same.append(site_items[i])
            if(len(not_same) != 0):
                header = { 'City': 'Update in ' + str(not_same[0]['post_number']), 'avrage price': -100 }
                content.add_header(header)
                content.add_contend(not_same)
                content_was_added = True
        else:
            site_data = get_data_from_site( user.min_price, user.max_price, user.min_rooms, zip_code )
            if len(site_data) == 0:
                continue
            avrage_price = find_avrage_price(site_data)
            best_priced = find_Best_Priced( site_data, user.best_search_pricecutof )
            tableRow = {
                'time' : datetime.today(),
                'No of appartments': str(len(site_data)),
                'City' : zip_code,
                'search term price': [user.min_price,user.max_price],
                'search term min rooms': 3,
                'avrage price': avrage_price,
                'best priced': best_priced
            }
            add_row_to_database(tableRow, Constnts.DB_CONNECTION_STRING, user.getUsername(), str(zip_code) )
            header = { 
                'City': tableRow['City'],
                'avrage price': tableRow['avrage price'] 
            }
            content.add_header(header)
            content.add_contend(tableRow['best priced'])
            content_was_added = True
    if content_was_added is True :
        if not os.path.exists('send_email_temps'):
            os.makedirs('send_email_temps')
        f = open( 'send_email_temps/' + user.getUsername() + '.html', 'w' )
        f.write(content.Html_Content())
        f.close()
        send_email(content.Html_Content(), user.email, 'Vel verðsettar íbúðir að skoða')
        print( str(datetime.today()) + ' Email sent to ' + user.getUsername() )

end_time = time.time()
print( str(datetime.today()) + ' Success exec time : %s Secounds' % (end_time - start_time) )
