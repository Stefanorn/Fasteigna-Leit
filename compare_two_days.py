import datetime

def compare_two_days(d1,d2):
    
    d1_id = []
    for dataset in d1:
        for d1_item in dataset['best priced']:
            d1_id.append(d1_item['id'])
    d2_id = []
    for dataset2 in d2:
        for d2_item in dataset2['best priced']:
            d2_id.append(d2_item['id'])

    if d1_id == d2_id:
        return True
    else:
        return False

day1 = [{ 'time': datetime.datetime(2019, 12, 21, 8, 0, 20, 469000), 'No of appartments': '26', 'City': '220', 'search term price': [1000000, 50000000], 'search term min rooms': 3, 'avrage price': 42157692.307692304, 'best priced': [{'id': '273811', 'link': 'http://fasteignir.visir.is/property/273811', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Háholt', 'rooms': '4 herbergi,  Fjölbýlishús', 'price': 40000000.0, 'squaremeter': 105.3, 'squareMeter_price': 379867.04653371323, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -22382.905077841308}, {'id': '279980', 'link': 'http://fasteignir.visir.is/property/279980', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Krókahraun', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 41900000.0, 'squaremeter': 93.6, 'squareMeter_price': 447649.5726495727, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -18984.063447953784}, {'id': '264458', 'link': 'http://fasteignir.visir.is/property/264458', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Ölduslóð seld', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 34000000.0, 'squaremeter': 83.8, 'squareMeter_price': 405727.923627685, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -90665.63297832367}, {'id': '233426', 'link': 'http://fasteignir.visir.is/property/233426', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Móabarð', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 37500000.0, 'squaremeter': 81.8, 'squareMeter_price': 458435.20782396087, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -31604.725760797097}, {'id': '277794', 'link': 'http://fasteignir.visir.is/property/277794', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Öldutún', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 32900000.0, 'squaremeter': 77.5, 'squareMeter_price': 424516.12903225806, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -43504.83231601154}]}, {'time': datetime.datetime(2019, 12, 21, 13, 13, 4, 888000), 'No of appartments': '26', 'City': '220', 'search term price': [1000000, 50000000], 'search term min rooms': 3, 'avrage price': 42157692.307692304, 'best priced': [{'id': '273811', 'link': 'http://fasteignir.visir.is/property/273811', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Háholt', 'rooms': '4 herbergi,  Fjölbýlishús', 'price': 40000000.0, 'squaremeter': 105.3, 'squareMeter_price': 379867.04653371323, 'image': 'http://api-beta.fasteignir.is/pictures/273811/8b8f1334faf2a7b81836b4e1a84d0c4d-469x310.jpg', 'Price Below Avrage': -22382.905077841308}, {'id': '279980', 'link': 'http://fasteignir.visir.is/property/279980', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Krókahraun', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 41900000.0, 'squaremeter': 93.6, 'squareMeter_price': 447649.5726495727, 'image': 'http://api-beta.fasteignir.is/pictures/279980/5ab36fb4eb1fadd7a6778a6cbc5e7424-469x310.jpg', 'Price Below Avrage': -18984.063447953784}, {'id': '264458', 'link': 'http://fasteignir.visir.is/property/264458', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Ölduslóð seld', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 34000000.0, 'squaremeter': 83.8, 'squareMeter_price': 405727.923627685, 'image': 'http://api-beta.fasteignir.is/pictures/264458/a679d36bad329a6a669e93d3e8466ca0-469x310.jpg', 'Price Below Avrage': -90665.63297832367}, {'id': '233426', 'link': 'http://fasteignir.visir.is/property/233426', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Móabarð', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 37500000.0, 'squaremeter': 81.8, 'squareMeter_price': 458435.20782396087, 'image': 'http://api-beta.fasteignir.is/pictures/233426/ef97506cdb2188c2a4cb4df558b08c01-469x310.jpg', 'Price Below Avrage': -31604.725760797097}, {'id': '277794', 'link': 'http://fasteignir.visir.is/property/277794', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Öldutún', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 32900000.0, 'squaremeter': 77.5, 'squareMeter_price': 424516.12903225806, 'image': 'http://api-beta.fasteignir.is/pictures/277794/17b80d2ba0eaf9c9f3a2685bc02d178e-469x310.jpg', 'Price Below Avrage': -43504.83231601154}]}]
day2 = [{ 'time': datetime.datetime(2019, 12, 21, 8, 0, 20, 469000), 'No of appartments': '26', 'City': '220', 'search term price': [1000000, 50000000], 'search term min rooms': 3, 'avrage price': 42157692.307692304, 'best priced': [{'id': '273811', 'link': 'http://fasteignir.visir.is/property/273811', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Háholt', 'rooms': '4 herbergi,  Fjölbýlishús', 'price': 40000000.0, 'squaremeter': 105.3, 'squareMeter_price': 379867.04653371323, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -22382.905077841308}, {'id': '279980', 'link': 'http://fasteignir.visir.is/property/279980', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Krókahraun', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 41900000.0, 'squaremeter': 93.6, 'squareMeter_price': 447649.5726495727, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -18984.063447953784}, {'id': '264458', 'link': 'http://fasteignir.visir.is/property/264458', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Ölduslóð seld', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 34000000.0, 'squaremeter': 83.8, 'squareMeter_price': 405727.923627685, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -90665.63297832367}, {'id': '233426', 'link': 'http://fasteignir.visir.is/property/233426', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Móabarð', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 37500000.0, 'squaremeter': 81.8, 'squareMeter_price': 458435.20782396087, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -31604.725760797097}, {'id': '277794', 'link': 'http://fasteignir.visir.is/property/277794', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Öldutún', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 32900000.0, 'squaremeter': 77.5, 'squareMeter_price': 424516.12903225806, 'image': 'https://i.imgur.com/OWLoorP.jpg', 'Price Below Avrage': -43504.83231601154}]}, {'time': datetime.datetime(2019, 12, 21, 13, 13, 4, 888000), 'No of appartments': '26', 'City': '220', 'search term price': [1000000, 50000000], 'search term min rooms': 3, 'avrage price': 42157692.307692304, 'best priced': [{'id': '273811', 'link': 'http://fasteignir.visir.is/property/273811', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Háholt', 'rooms': '4 herbergi,  Fjölbýlishús', 'price': 40000000.0, 'squaremeter': 105.3, 'squareMeter_price': 379867.04653371323, 'image': 'http://api-beta.fasteignir.is/pictures/273811/8b8f1334faf2a7b81836b4e1a84d0c4d-469x310.jpg', 'Price Below Avrage': -22382.905077841308}, {'id': '279980', 'link': 'http://fasteignir.visir.is/property/279980', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Krókahraun', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 41900000.0, 'squaremeter': 93.6, 'squareMeter_price': 447649.5726495727, 'image': 'http://api-beta.fasteignir.is/pictures/279980/5ab36fb4eb1fadd7a6778a6cbc5e7424-469x310.jpg', 'Price Below Avrage': -18984.063447953784}, {'id': '264458', 'link': 'http://fasteignir.visir.is/property/264458', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Ölduslóð seld', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 34000000.0, 'squaremeter': 83.8, 'squareMeter_price': 405727.923627685, 'image': 'http://api-beta.fasteignir.is/pictures/264458/a679d36bad329a6a669e93d3e8466ca0-469x310.jpg', 'Price Below Avrage': -90665.63297832367}, {'id': '233426', 'link': 'http://fasteignir.visir.is/property/233426', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Móabarð', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 37500000.0, 'squaremeter': 81.8, 'squareMeter_price': 458435.20782396087, 'image': 'http://api-beta.fasteignir.is/pictures/233426/ef97506cdb2188c2a4cb4df558b08c01-469x310.jpg', 'Price Below Avrage': -31604.725760797097}, {'id': '277794', 'link': 'http://fasteignir.visir.is/property/277794', 'post_number': '220 Hafnarfjörður', 'street_Address': 'Öldutún', 'rooms': '3 herbergi,  Fjölbýlishús', 'price': 32900000.0, 'squaremeter': 77.5, 'squareMeter_price': 424516.12903225806, 'image': 'http://api-beta.fasteignir.is/pictures/277794/17b80d2ba0eaf9c9f3a2685bc02d178e-469x310.jpg', 'Price Below Avrage': -43504.83231601154}]}]
print(compare_two_days(day1,day2))