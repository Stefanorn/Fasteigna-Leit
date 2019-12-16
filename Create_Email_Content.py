import re

def _readable_large_number(large_number):
    large_number = large_number[::-1]
    large_number = '.'.join(large_number[i:i+3] for i in range(0, len(large_number), 3))
    return large_number[::-1]
class Create_Email_Content(object):

    def __init__(self, body=None, header=None):
        self.body = body
        self.header = header
        self.res = self._generate_head()

        if self.header is not None:
            self.add_header(header)
        if self.body is not None:
            self.add_contend(body)


    def Html_Content(self):
        return self.res + self._generate_fooder()
    def add_contend(self, body):
        for item in body:
            price = _readable_large_number(str(int(item['price'])))
            m2_price = _readable_large_number(str(int(item['squareMeter_price'])))

            body = self._generate_item()
            body = re.sub(r'&&_street_address_&&',item['street_Address'], body)
            body = re.sub(r'&&_rooms_&&', item['rooms'], body)
            body = re.sub(r'&&_price_&&', 'Verð : ' + price + ' kr', body)
            body = re.sub(r'&&_size_&&', 'Stærð : ' + str(int(item['squaremeter'])) + ' m2', body)
            body = re.sub(r'&&_price_per_m2_&&', 'fermetraverð ' + m2_price + ' kr', body)
            body = re.sub(r'&&_link_&&', item['link'], body)
            body = re.sub(r'&&_image_&&', item['image'], body)
            self.res += body
    def add_header(self, header):
        avg_price = _readable_large_number(str(int(header['avrage price'])))
        headline = self._generate_headLine()
        headline = re.sub(r'&&_postalCode_&&', header['City'], headline)
        headline = re.sub(r'&&_avrage_price_&&', "Meðalverð er : " + avg_price + " kr", headline)
        self.res += headline

    def _generate_head(self):
        f = open('./emailTemplate/head.html')
        return f.read()
    def _generate_headLine(self):
        f = open('./emailTemplate/headline.html')
        return f.read()
    def _generate_item(self):
        f = open('./emailTemplate/item.html')
        return f.read()
    def _generate_fooder(self):
        f = open('./emailTemplate/fooder.html')
        return f.read()
