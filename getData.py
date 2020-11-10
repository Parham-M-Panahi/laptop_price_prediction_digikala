# get product data
# input : web data  &  id.txt
# output : products.json

from bs4 import BeautifulSoup as bs
import requests
import re
import json
import random
import time

URL = 'https://www.digikala.com/product/dkp-{}'


def getdata():

    print('Scanning for product data.')

    # product keys
    keys = []
    with open('id.txt', 'r') as f:
        for line in f:
            keys.append(line.strip())

    # shuffle keys to draw uniform samples
    random.shuffle(keys)

    # keys with bad html format - to be deleted after scanning
    faulty_keys = []

    # to be filled with product data
    productdata = {}

    counter = 1
    for id in keys:
        # sleep for 3 sec not to overload the server
        time.sleep(3)

        try:

            # add url
            productdata[id] = {'url': URL.format(id)}

            # connect to url
            try:
                r = requests.get(productdata[id]['url'])
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                print('failed {}/{}'.format(counter, len(keys)))
                counter += 1
                continue

            soup = bs(r.text, 'html.parser')
            specs = list(soup.find('div', attrs={'id':'tabs'}).div.children)[1].article

            # add product name
            productdata[id]['name'] = specs.find('h2', attrs={'class': 'c-params__headline'}).span.text.strip()

            # add product price
            productdata[id]['price'] = soup.find('div', attrs={'class':'c-product__seller-price-pure js-price-value'}).text.strip()

            # add product specs
            for section in specs.find_all('section')[:6]:
                # find section name
                if section.h3.find('a'):
                    sectionName = section.h3.span.a.text.strip()
                else:
                    sectionName = section.h3.text.strip()
                
                productdata[id][sectionName] = {}

                for li in section.ul.children:
                    #key
                    keytag = li.find('div', attrs={'class': 'c-params__list-key'})
                    if keytag.find('a'):
                        key = keytag.span.a.text.strip()
                    else:
                        key = keytag.span.text.strip()
                    #value
                    valtag = li.find('div', attrs={'class': 'c-params__list-value'})
                    if valtag.find('a'):
                        val = valtag.span.span.a.text.strip()
                    else:
                        val = valtag.span.text.strip()

                    productdata[id][sectionName][key] = val

        except AttributeError:
            # handle bad html formats
            faulty_keys.append(id)
            continue

        print('{}/{}'.format(counter, len(keys)))
        counter += 1

    # remove products with bad html format
    for key in faulty_keys:
        if key in productdata:
            del productdata[key]


    # write product data to json
    with open('products.json', 'w', encoding='utf8') as f:
        json.dump(productdata, f, ensure_ascii=False)


    print('Scanned {} products. stored into products.json .\n'.format(len(productdata)))



if __name__=='__main__':
    getdata()