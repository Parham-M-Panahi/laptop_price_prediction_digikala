import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
import numpy as np
import math
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


MYSQL_PASSWORD = '0000'	# PUT UR SQL PASSWORD HERE


def readTable(host='localhost', user='root', password=MYSQL_PASSWORD, db='finalprojectdb', table='laptopdata'):
    with mysql.connector.connect(host=host, user=user, password=password, database=db) as con:
        with con.cursor() as cur:
            cur.execute('select * from {};'.format(table))
            rows = cur.fetchall()

            cur.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N\'laptopdata\';')
            columns = list(map(lambda x: x[0], cur.fetchall()))


        df = pd.DataFrame(rows, columns=columns)

    return df


def cleanDf(df):
 
    # removing weight outliers
    df = df[df['Weight'] < 5]

    # Creating 4 feafures by combining data from cpu,ram,display,wight
    density = df['Weight'] / df['DisplaySize']
    resolution = ((df['DisplayPixelWidth']*df['DisplayPixelHeight']) / ((144.0/337.0) * (df['DisplaySize'] ** 2)).astype('int')).astype('int')
    density.name = 'Density'
    resolution.name = 'Resolution'
    p = df['Price'] / 1000000
    p.name = 'Price'
    CPU = df['CPUSpeed'] * df['CPUCacheSize']
    tmp = df.replace({'RAMTechnology':{'DDR3':3, 'DDR4':4}},inplace=False)['RAMTechnology']
    RAM = df['RAMCapacity'] * tmp
    CPU.name = 'CPU'
    RAM.name = 'RAM'
    data = {'Density':density , 'Resolution':resolution , 'CPU':CPU, 'RAM':RAM, 'Price':p}
    d = pd.concat(data, axis = 1)

    return d

def getDisplaySize():
    flag = True
    while flag:
        print('DisplaySize:  1. 13.3\'  2. 15.6\'  3. 17.3\'')
        i = input('> ')
        if i == '1':
            temp = 13.3
            flag = False
            pass
        elif i == '2':
            temp = 15.6
            flag = False
            pass
        elif i == '3':
            temp = 17.3
            flag = False
            pass
        else:
            print('Wrong input try again: ')

    return temp


def getDisplayResolution():
    flag = True
    while flag:
        print('DisplayResolution:  1. HD  2. FULL-HD  3. 4K')
        i = input('> ')
        if i == '1':
            temp = 1049088
            flag = False
            pass
        elif i == '2':
            temp = 2073600
            flag = False
            pass
        elif i == '3':
            temp = 8294400
            flag = False
            pass
        else:
            print('Wrong input try again: ')

    return temp


def getCPUSpeed():
    flag = True
    while flag:
        print('CPU base clock:  1. 2.0 gHz  2. 2.2 gHz  3. 2.8 gHz')
        i = input('> ')
        if i == '1':
            temp = 2.0
            flag = False
            pass
        elif i == '2':
            temp = 2.2
            flag = False
            pass
        elif i == '3':
            temp = 2.8
            flag = False
            pass
        else:
            print('Wrong input try again: ')

    return temp


def getCPUCache():
    flag = True
    while flag:
        print('CPU Cache :  1. 2mb  2. 4mb  3. 8mb  4. 12mb')
        i = input('> ')
        if i == '1':
            temp = 2
            flag = False
            pass
        elif i == '2':
            temp = 4
            flag = False
            pass
        elif i == '3':
            temp = 8
            flag = False
            pass
        elif i == '4':
            temp = 12
            flag = False
            pass
        
        else:
            print('Wrong input try again: ')

    return temp


def getRAMSize():
    flag = True
    while flag:
        print('RAM :  1. 4gb  2. 8gb  3. 16gb  4. 32gb  5. 64gb')
        i = input('> ')
        if i == '1':
            temp = 4
            flag = False
            pass
        elif i == '2':
            temp = 8
            flag = False
            pass
        elif i == '3':
            temp = 16
            flag = False
            pass
        elif i == '4':
            temp = 32
            flag = False
            pass
        elif i == '5':
            temp = 64
            flag = False
            pass
        
        else:
            print('Wrong input try again: ')

    return temp



def getRAMTechnology():
    flag = True
    while flag:
        print('RAM Technology :  1. DDR3    2. DDR4')
        i = input('> ')
        if i == '1':
            temp = 3
            flag = False
            pass
        elif i == '2':
            temp = 4
            flag = False
            pass
        
        else:
            print('Wrong input try again: ')

    return temp




def predict(model):
    print('Please select laptop specs by typing the number of each option')

    # Display
    ds = getDisplaySize()
    dr = getDisplayResolution()

    resolution = dr / ((144.0/337.0) * (ds ** 2))
    # use average weight
    density = 1.993792 / ds


    cs = getCPUSpeed()
    cc = getCPUCache()
    CPU = cs * cc

    rs = getRAMSize()
    rt = getRAMTechnology()
    RAM = rs * rt


    
    # print(resolution)
    # print(density)
    # print(RAM)
    # print(CPU)

    data = [density, resolution, CPU, RAM]

    print('Price Prediction is : %.2f million tomans' % model.predict([data])[0])


def main():

    df = readTable()

    d = cleanDf(df)

    # pd.plotting.scatter_matrix(d, alpha=0.6)
    # plt.show()

    x = d[[ 'Density' , 'Resolution'  , 'CPU' , 'RAM']]
    y = d['Price']

    # print(d)


    # due to low number of data point, re run the algorithm 100 times and choose the best model
    best_model = None
    best_mse = math.inf
    for _ in range(100):

        # spliting data for test/train
        train_data, test_data, train_label, test_label = train_test_split(x,y,test_size = 0.1)
        
        # creating the model
        model = DecisionTreeRegressor(max_depth=20, min_samples_leaf=0.01, random_state=3)

        # Train the Model
        model.fit(train_data, train_label)

        # Validation
        pred_label = model.predict(test_data)
        mse = mean_squared_error(test_label, pred_label)

        # choose the best model
        if mse < best_mse:
            best_model = model
            best_mse = mse  

        print('.', end='')
    print()



    print('Model\' MSE = %.2f' % best_mse)

    # make prediction
    data = [0.1, 70, 20, 8]
    predict(best_model)
    # print(test_data, model.predict(test_data))



if __name__=='__main__':
    main()