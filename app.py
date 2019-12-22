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
from datetime import datetime, timedelta
import time
from Create_Email_Content import Create_Email_Content
from Constnts import Constnts
from scrape_website import scrape_website

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
def update_array_in_row(row_id,data, connection_string, database, collection ):
    mng_client = pymongo.MongoClient(connection_string)
    mng_db = mng_client[database]
    db_cm = mng_db[collection]
    db_cm.update_one({'_id': row_id },
                    { '$push': { 'new items today' : data } } )


def add_row_to_database(table_row, connection_string, database, collection ):
    mng_client = pymongo.MongoClient(connection_string)
    mng_db = mng_client[database]
    db_cm = mng_db[collection]
    db_cm.insert_one(table_row)
def compare_two_days(d1,d2):
    d1_id = []
    for dataset in d1:
        if len(dataset) == 0:
            continue
        for d1_item in dataset[0]['best priced']:
            d1_id.append(d1_item['id'])
    d2_id = []
    for dataset2 in d2:
        if len(dataset2) == 0:
            continue
        for d2_item in dataset2[0]['best priced']:
            d2_id.append(d2_item['id'])
    print(d1_id)
    print(d2_id)
    if d1_id == d2_id:
        print ('true')
        return True
    else:
        print ('false')

        return False
def Get_rows_from_today(connection_string, database, collection, today):

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
    msg['Subject'] = zip_code 
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
    all_today_rows = []
    all_yesterday_rows = []
    for zip_code in user.zip_codes:
        username = user.getUsername()
        today = datetime.today()
        yesterday = today - timedelta(days = 1)
        today_rows = Get_rows_from_today(Constnts.DB_CONNECTION_STRING, username, zip_code , today)

        all_yesterday_rows.append(Get_rows_from_today(Constnts.DB_CONNECTION_STRING, username, zip_code , yesterday))
        all_today_rows.append(Get_rows_from_today(Constnts.DB_CONNECTION_STRING, username, zip_code , today))

        site_data = get_data_from_site( user.min_price, user.max_price, user.min_rooms, zip_code )
        if len(site_data) == 0:
            print( str(datetime.today()) + ' no items in ' + user.getUsername() + ' ' + str(zip_code))
            continue
        ## I have already added to db today so i will check if there is something new
        if len(today_rows) >= 1:
            print( str(datetime.today()) + ' already added to db '+ user.getUsername() + ' ' + str(zip_code) + ' today.')
            db_items = today_rows[0]['best priced']
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
                if 'new items today' in today_rows[0].keys():
                    for item in today_rows[0]['new items today']:
                        site_items_ids = []
                        for id in site_items:
                            site_items_ids.append(int(id['id']))
                        if int(item['id']) in site_items_ids:
                            print( str(datetime.today()) + ' This item is not new ' + user.getUsername() + ' ' + str(zip_code) + ' ')
                        else:
                            print( str(datetime.today()) + ' this item is new i will add to new items and send email to ' + user.getUsername() + ' ' + str(zip_code) + ' ')
                            header = { 'City': 'Update in ' + str(not_same[0]['post_number']), 'avrage price': -100 }
                            content.add_header(header)
                            content.add_contend(not_same)
                            content_was_added = True
                            update_array_in_row(today_rows[0]['_id'], item, Constnts.DB_CONNECTION_STRING, user.getUsername(), str(zip_code) )
                else:
                    print( str(datetime.today()) + ' this item is new i will add to new items and send email to ' + user.getUsername() + ' ' + str(zip_code) + ' ')

                    header = { 'City': 'Update in ' + str(not_same[0]['post_number']), 'avrage price': -100 }
                    content.add_header(header)
                    content.add_contend(not_same)
                    content_was_added = True
                    for item in not_same:
                        update_array_in_row(today_rows[0]['_id'], item, Constnts.DB_CONNECTION_STRING, user.getUsername(), str(zip_code) )
    

        ## I will add to db
        else:
            print( str(datetime.today()) + ' adding to database '+ user.getUsername() + ' ' + str(zip_code) )
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
            print( str(datetime.today()) + ' added new row to database ' + user.getUsername() + ' ' + str(zip_code))

    if content_was_added is True and compare_two_days(all_today_rows,all_yesterday_rows) is False :
        if not os.path.exists('send_email_temps'):
            os.makedirs('send_email_temps')
        f = open( 'send_email_temps/' + user.getUsername() + '.html', 'w' )
        f.write(content.Html_Content())
        f.close()
        send_email(content.Html_Content(), user.email, 'Vel verðsettar íbúðir að skoða')
        print( str(datetime.today()) + ' Email sent to ' + user.getUsername() )

end_time = time.time()
print( str(datetime.today()) + ' Success exec time : %s Secounds' % (end_time - start_time) )
