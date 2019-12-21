from Create_Email_Content import Create_Email_Content
bodyTemp = [{
            "id" : 123,
            "link" : 'www.hugi.is',
            "post_number" : '221 hafnavík',
            "street_Address" : 'StebbaStraeti',
            "rooms": '2 rooms apartment',
            "price" : 20000000.2,
            "squaremeter": 100,
            "squareMeter_price": 500000,
            "image": "https://i.imgur.com/OWLoorP.jpg"
        },
        {
            "id" : 123,
            "link" : 'www.hugi.is',
            "post_number" : '221',
            "street_Address" : 'stöffgata',
            "rooms": '2',
            "price" : 21.2,
            "squaremeter": 233,
            "squareMeter_price": 232,
            "image": "https://i.imgur.com/OWLoorP.jpg"
        },
        {
            "id" : 123,
            "link" : 'www.hugi.is',
            "post_number" : '221',
            "street_Address" : 'stöffgata',
            "rooms": '2',
            "price" : 21.2,
            "squaremeter": 233,
            "squareMeter_price": 232,
            "image": "https://i.imgur.com/OWLoorP.jpg"
        }]

headTemp = {
    'City' : '201',
    'avrage price': 12344
}

cle = Create_Email_Content(bodyTemp,headTemp)

cle.add_header(headTemp)
cle.add_contend(bodyTemp)

print(cle.Html_Content())