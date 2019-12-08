import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import json
import pymongo
import csv
import smtplib
from email.message import EmailMessage

### TODO ætti að breyta þessu í margar skrár
### TODO það þirfti að laga öll breytunöfn hafa samræmi þetta er sick


## TODO þarf að gera enviroment breytur
class Constnts:
    EMAIL_ADDRESS = "ekkisvara69@gmail.com"
    EMAIL_PASSWORD = "Geirfinnur54"
    DB_CONNECTION_STRING = 'mongodb+srv://admin:prumpusvin44329@cluster0-xepqq.mongodb.net'

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
            print( "Log message -- cannot scrape item " + link )
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
        }
        allProps.append(prop)
    return allProps


##################################################################
#  Data_manipulation_functions
##################################################################
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
    return totalSum / len(data)
def find_biggest_propertys(data,index):
    data.sort(key=sort_by_sqaremeter,reverse=True)
    return data[:index]


##################################################################
#  Data_gathering exporting
##################################################################
def add_row_to_database(table_row, connection_string, database, collection ):
    mng_client = pymongo.MongoClient(connection_string)
    mng_db = mng_client[database]
    db_cm = mng_db[collection]
    db_cm.insert_one(table_row)

def print_to_console(data):
    print(data['City'])
    print('Avrage price is ' + str(int(data['avrage price'])) + ' kr')
    print('')
    print( str(len(data['lowest price'])) + ' lowest priced propertys are:')
    print('------------------------------')
    for item in data['lowest price']:
        print(item['street_Address'] + ', ' + item['rooms'])
        print('price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2')
        print('price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' )
        print('link -- '  + item['link'] )
        print()
    print('------------------------------')

    print( str(len(data['Cheepest Square meter price'])) + ' Cheepset m2 propertys are:')
    print('------------------------------')
    for item in data['Cheepest Square meter price']:
        print(item['street_Address'] + ', ' + item['rooms'])
        print('price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2')
        print('price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' )
        print('link -- '  + item['link'] )
        print()
    print('------------------------------')

    print( str(len(data['largest property'])) + ' largest propertys are:')
    print('------------------------------')
    for item in data['largest property']:
        print(item['street_Address'] + ', ' + item['rooms'])
        print('price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2')
        print('price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' )
        print('link -- '  + item['link'] )
        print()
    print('------------------------------')
    print('Search term ')
    print('pricepoint from ' + str(int(data['search term price'][0])) + " kr to " + str(int(data['search term price'][1])) + " kr" )
    print('min rooms ' + str(int(data['search term min rooms'])) )

def generate_single_property_html( street_Address, rooms, price, squaremeter, squareMeter_price, link ):
    retString = ''
    retString += street_Address + ', ' + rooms + '\n'
    retString += 'price - ' + price + ' kr, size - ' + squaremeter + ' m2' + '\n'
    retString += 'price/m2 - ' + squareMeter_price + ' kr/m2' + '\n'
    retString += 'link -- '  + link + '\n\n'
    return retString
## TODO klára þetta henda inn html tögum
def generate_generic_HTML_text(data):
    retString = ''
    retString += data['City'] + '\n'
    retString += 'Avrage price is ' + str(int(data['avrage price'])) + ' kr' + '\n'
    retString += '\n'
    retString += str(len(data['lowest price'])) + ' lowest priced propertys are:' + '\n'
    retString += '------------------------------' + '\n'
    for item in data['lowest price']:
        retString += generate_single_property_html( item['street_Address'],item['rooms'], str(int(item['price'])), str(int(item['squaremeter'])), str(int(item['squareMeter_price'])), item['link'] )
    retString += '------------------------------' + '\n'

    retString +=  str(len(data['Cheepest Square meter price'])) + ' Cheepset m2 propertys are:' + '\n'
    retString += '------------------------------' + '\n'
    for item in data['Cheepest Square meter price']:
        retString += generate_single_property_html( item['street_Address'],item['rooms'], str(int(item['price'])), str(int(item['squaremeter'])), str(int(item['squareMeter_price'])), item['link'] )
    retString += '------------------------------'+ '\n'

    retString +=  str(len(data['largest property'])) + ' largest propertys are:'+ '\n'
    retString += '------------------------------' + '\n'
    for item in data['largest property']:
        retString += generate_single_property_html( item['street_Address'],item['rooms'], str(int(item['price'])), str(int(item['squaremeter'])), str(int(item['squareMeter_price'])), item['link'] )
    retString += '------------------------------' + '\n'
    retString += 'Search term ' + '\n'
    retString += 'pricepoint from ' + str(int(data['search term price'][0])) + " kr to " + str(int(data['search term price'][1])) + " kr" + '\n'
    retString += 'min rooms ' + str(int(data['search term min rooms'])) + '\n'
    return retString
def generate_generic_text(data):
    retString = ''
    retString += data['City'] + '\n'
    retString += 'Avrage price is ' + str(int(data['avrage price'])) + ' kr' + '\n'
    retString += '\n'
    retString += str(len(data['lowest price'])) + ' lowest priced propertys are:' + '\n'
    retString += '------------------------------' + '\n'
    for item in data['lowest price']:
        retString += item['street_Address'] + ', ' + item['rooms'] + '\n'
        retString += 'price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2' + '\n'
        retString += 'price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' + '\n'
        retString += 'link -- '  + item['link']  + '\n'
        retString += '\n'
    retString += '------------------------------' + '\n'

    retString +=  str(len(data['Cheepest Square meter price'])) + ' Cheepset m2 propertys are:' + '\n'
    retString += '------------------------------' + '\n'
    for item in data['Cheepest Square meter price']:
        retString += item['street_Address'] + ', ' + item['rooms'] + '\n'
        retString += 'price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2' + '\n'
        retString += 'price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' + '\n'
        retString += 'link -- '  + item['link'] + '\n'
        retString += '\n'
    retString += '------------------------------'+ '\n'

    retString +=  str(len(data['largest property'])) + ' largest propertys are:'+ '\n'
    retString += '------------------------------' + '\n'
    for item in data['largest property']:
        retString += item['street_Address'] + ', ' + item['rooms'] + '\n'
        retString += 'price - ' + str(int(item['price'])) + ' kr, size - ' + str(int(item['squaremeter'])) + ' m2' + '\n'
        retString += 'price/m2 - ' + str(int(item['squareMeter_price'])) + ' kr/m2' + '\n'
        retString += 'link -- '  + item['link'] + '\n'
        retString +=  '\n'
    retString += '------------------------------' + '\n'
    retString += 'Search term ' + '\n'
    retString += 'pricepoint from ' + str(int(data['search term price'][0])) + " kr to " + str(int(data['search term price'][1])) + " kr" + '\n'
    retString += 'min rooms ' + str(int(data['search term min rooms'])) + '\n'
    return retString
def send_email(data):
    EMAIL_ADDRESS = Constnts.EMAIL_ADDRESS
    EMAIL_PASSWORD = Constnts.EMAIL_PASSWORD
    msg = EmailMessage()
    msg['Subject'] = 'Áhugaverdar Ibudir'
    msg['From'] = 'ekkisvara69@gmail.com'
    msg['To'] = 'stefanorn92@gmail.com'
    content = generate_generic_text(data)
    msg.set_content( content )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

def generate_csv(data):
    csv_file = open('temp.csv','w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['number','link','street', 'rooms', 'price', 'size', 'price/m2'])
    for item in data['lowest price']:
        csv_writer.writerow([
            '1',
            item['link'],
            item['street_Address'],
            item['rooms'],
            str(int(item['price'])),
            str(int(item['squaremeter'])),
            str(int(item['squareMeter_price']))
            ])
    csv_file.close()

# TODO laga harðkóðun hér þetta þessar breytur eru aldrei notaðar
# TODO gera fall sem sendir þessar requestur og skilar hreinu htmli eða scrapuðu data
price_point=[1000000,50000000]
min_rooms=3
hfj_requests = [
    'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip=221&category=1,2,4,7&price=1000000,50000000&room=3,10&itemcount=60&page=1',
    'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip=221&category=1,2,4,7&price=1000000,50000000&room=3,10&itemcount=60&page=2',
    'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip=221&category=1,2,4,7&price=1000000,50000000&room=3,10&itemcount=60&page=3',
    'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip=221&category=1,2,4,7&price=1000000,50000000&room=3,10&itemcount=60&page=4',
    'http://fasteignir.visir.is/ajaxsearch/getresults?stype=sale&zip=221&category=1,2,4,7&price=1000000,50000000&room=3,10&itemcount=60&page=5']

hfj_data = []
for req in hfj_requests:
    res = requests.get(req).text
    data = scrape_website(res)
    hfj_data = hfj_data + data

## TODO þetta ætti að vera fall
lowest_price_hfj = find_lowest_prices(hfj_data, 10)
cheepse_m2 = find_cheepes_squaremeter(hfj_data,5)
avrage_price = find_avrage_price(hfj_data)
largest_property = find_biggest_propertys(hfj_data,5)

tableRow = {
    'City' : hfj_data[0]['post_number'],
    'search term price': [1000000,50000000],
    'search term min rooms': 3,
    'avrage price': avrage_price,
    'Cheepest Square meter price' : cheepse_m2,
    'lowest price' : lowest_price_hfj,
    'largest property': largest_property,
    'All data': hfj_data
}

#print_to_console(tableRow)
#generate_csv(tableRow)
print('Found '+ str(len(tableRow['All data'])) + ' items')
print('adding data to db')
add_row_to_database(tableRow, Constnts.DB_CONNECTION_STRING, 'fasteignir', 'hafnafjordur' )
print('data added\nsending email')
send_email(tableRow)
print('emailSent')