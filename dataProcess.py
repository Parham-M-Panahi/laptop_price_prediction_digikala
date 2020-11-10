# uses products.json file and cleans up the data to be used in machine learning
# input : products.json
# output : processed.csv

import json
import re
import csv


# fixer upper functions

def fixPrice(price):
    f2eDigit = { 
        '۰':'0',
        '۱':'1',
        '۲':'2',
        '۳':'3',
        '۴':'4',
        '۵':'5',
        '۶':'6',
        '۷':'7',
        '۸':'8',
        '۹':'9',
        '۰':'0',
        ',':''
    }

    for digit in f2eDigit.keys():
        price = price.replace(digit, f2eDigit[digit])

    return price

def extractDigit(s):
    return re.search(r'([\d\.]+)', s).group(1)

def extractPixelCount(s):
    r = re.search(r'(\d+)\s*x(\d+)', s)
    return r.group(1), r.group(2)


def cleaner():
    # open products.json

    with open('products.json', 'r') as f:
        data = json.loads(f.read())



    # write to processed.csv

    with open('processed.csv', mode='w', newline='') as csvfile:
        writer =  csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # csv header
        writer.writerow(['ProductID', 'Price', 'Weight', 'DisplaySize', 'DisplayPixelWidth', 'DisplayPixelHeight', 'CPUCompany', 'CPUModel', 'CPUSpeed', 'CPUCacheSize', 'RAMCapacity', 'RAMTechnology'])
        for key in data:
            try:
                    
                print(key)
                # print('Product name : {}'.format(data[key]['name']))

                
                p = fixPrice(data[key]['price'])

                print('Price : {}'.format(p))

                # weight
                w = extractDigit(data[key]['مشخصات فیزیکی']['وزن'])

                print('Product Weight {}'.format(w))

                # display
                print('display data : ')

                ds = extractDigit(data[key]['صفحه نمایش']['اندازه صفحه نمایش'])

                print(ds)

                dr = data[key]['صفحه نمایش']['دقت صفحه نمایش']

                dw, dh = extractPixelCount(dr)

                print(dw)
                print(dh)


                # cpu
                print('CPU data : ')

                cpu = data[key]['پردازنده مرکزی']['سازنده پردازنده']
                print(cpu)

                try:
                    cpus = extractDigit(data[key]['پردازنده مرکزی']['محدوده سرعت پردازنده'])
                except KeyError:
                    cpus = None
                print(cpus)

                cpum = data[key]['پردازنده مرکزی']['سری پردازنده']
                print(cpum)

                try:
                    cpuc = extractDigit(data[key]['پردازنده مرکزی']['حافظه Cache'])
                except KeyError:
                    cpuc = None
                print(cpuc)



                # ram
                print('RAM data : ')

                ram = extractDigit(data[key]['حافظه RAM']['ظرفیت حافظه RAM'])
                print(ram)
        
                ramd = data[key]['حافظه RAM']['نوع حافظه RAM']
                print(ramd)


                print('***************************************************')
                # write this produc to csv
                writer.writerow([key, p, w, ds, dw, dh, cpu, cpum, cpus, cpuc, ram, ramd])
            except KeyError:
                continue



if __name__=='__main__':
    cleaner()