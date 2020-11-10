# scans digikala for laptop id
# input : web data
# output : id.txt

from bs4 import BeautifulSoup as bs
from requests import get
import re
import time

MAX_PAGE = 8
URL = 'https://www.digikala.com/search/category-notebook-netbook-ultrabook/?has_selling_stock=1&pageno={}&sortby=4'


def getid():

    print('Scanning for id list.   MAX_PAGE = {}'.format(MAX_PAGE))
    productIds = []

    pattern = re.compile(r'/dkp-(\d*)/') 

    for i in range(1, MAX_PAGE + 1):
        # sleep to avoid server block
        time.sleep(3)

        r = get(URL.format(i))
        soup = bs(r.text, 'html.parser')


        products = soup.find('ul', attrs={'class':'c-listing__items js-plp-products-list'})
        for li in products.children:
            href = li.div.a.get('href')
            # productUrls.append(li.div.a.get('href'))
            productIds.append(re.search(pattern, href).group(1))

        print('.')

    with open('id.txt', 'w') as f :
        for id in productIds:
            f.write(id+'\n')

    print('Scanned {} id. stored into id.txt .\n'.format(len(productIds)))

if __name__=='__main__':
    getid()