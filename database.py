# input : processed.csv
# output : mysql database with the data stored within

import csv
import mysql.connector

MYSQL_PASSWORD = '0000'	# PUT UR SQL PASSWORD HERE

def csv2DB(filepath):

    with mysql.connector.connect(host='127.0.0.1', user='root', password=MYSQL_PASSWORD) as db:
        with db.cursor() as cur:
            cur.execute('CREATE DATABASE IF NOT EXISTS finalprojectdb;')
            cur.execute('USE finalprojectdb;')
            
            with open(filepath, mode='r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                header = True
                for row in reader:
                    if header:
                        q = 'CREATE TABLE IF NOT EXISTS laptopdata (ProductID INT NOT NULL UNIQUE, Price INT, Weight FLOAT, DisplaySize FLOAT, DisplayPixelWidth INT, DisplayPixelHeight INT, CPUCompany VARCHAR(64), CPUModel VARCHAR(64), CPUSpeed FLOAT, CPUCacheSize INT, RAMCapacity INT, RAMTechnology VARCHAR(64));'
                        cur.execute(q)
                        header = False
                        continue

                    row[0] = int(row[0])
                    # print(tuple(row))
                    try:
                        mysql.connector.errors.IntegrityError
                        try:
                            cur.execute('INSERT INTO laptopdata VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', tuple(row))
                        except mysql.connector.errors.IntegrityError:
                            continue
                    except mysql.connector.errors.DataError:
                        print('Dropping missing data:')
                        print(row)

                db.commit()


if __name__=='__main__':
    csv2DB('processed.csv')