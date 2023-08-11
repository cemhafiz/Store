import pandas as pd
import numpy as np
import sys
from datetime import timedelta, datetime, date
import csv

if sys.argv[1] != "--min-date" and sys.argv[3] != "--max-date":
    print("You entered wrong arguments! (1st argument expected: --min-date, 2nd argument expected: --max-date)")
else:
    try:
        min_date = pd.to_datetime(sys.argv[2])
        max_date = pd.to_datetime(sys.argv[4])

        brand = pd.read_csv('brand.csv')
        product = pd.read_csv('product.csv')
        sales = pd.read_csv('sales.csv')
        store = pd.read_csv('store.csv')

        sales['date']= pd.to_datetime(sales['date'])

        result = pd.DataFrame(columns=['product_id', 'store_id', 'brand_id', 'date', 'sales_product', 
        'MA7_P', 'LAG7_P', 'sales_brand', 'MA7_B', 'LAG7_B', 'sales_store', 'MA7_S', 'LAG7_S'])

        for i in range(len(sales)):
            if sales['date'][i] - min_date >= timedelta(0) and max_date - sales['date'][i] >= timedelta(0):
                sales_brand = 0

                list = sales.index[(sales['date'] == sales['date'][i]) & (brand.index[product['brand'][sales['product'][i]] == brand['name']])].tolist()

                for j in range(len(list)):
                    sales_brand += sales['quantity'][list[j]]

                sales_store = 0
                
                list = sales.index[(sales['date'] == sales['date'][i]) & (sales['store'] == sales['store'][i])].tolist()

                for j in range(len(list)):
                    sales_store += sales['quantity'][list[j]]

                MA7_P = 0.0

                for j in range(7):
                    MA7_P += sales['quantity'][i - j - 1]
                
                MA7_P = MA7_P / 7

                LAG7_P = sales['quantity'][i - 7]
                
                MA7_B = 0.0

                list = sales.index[((sales['date'][i] == sales['date'][i] - timedelta(1)) | (sales['date'][i] == sales['date'][i] - timedelta(2)) | (sales['date'][i] == 
                sales['date'][i] - timedelta(3)) | (sales['date'][i] == sales['date'][i] - timedelta(4)) | (sales['date'][i] == sales['date'][i] - timedelta(5)) | 
                (sales['date'][i] == sales['date'][i] - timedelta(6)) | (sales['date'][i] == sales['date'][i] - timedelta(7))) & (sales['store'] == sales['store'][i]) & 
                (brand.index[product['brand'][sales['product'][i]] == brand['name']])].tolist()

                for j in range(len(list)):
                    MA7_B += store['quantity'][list[j]]

                MA7_B = MA7_B / 7

                LAG7_B = 0

                list = sales.index[(sales['date'] == sales['date'][i] - timedelta(7)) & (brand.index[product['brand'][sales['product'][i]] == brand['name']])].tolist()

                for j in range(len(list)):
                    LAG7_B += sales['quantity'][list[j]]
                
                MA7_S = 0.0
                
                list = sales.index[((sales['date'][i] == sales['date'][i] - timedelta(1)) | (sales['date'][i] == sales['date'][i] - timedelta(2)) | (sales['date'][i] == 
                sales['date'][i] - timedelta(3)) | (sales['date'][i] == sales['date'][i] - timedelta(4)) | (sales['date'][i] == sales['date'][i] - timedelta(5)) | 
                (sales['date'][i] == sales['date'][i] - timedelta(6)) | (sales['date'][i] == sales['date'][i] - timedelta(7))) & (sales['store'] == sales['store'][i]) & 
                (brand.index[product['brand'][sales['product'][i]] == brand['name']]) & sales['product'] == sales['product'][i]].tolist()

                for j in range(len(list)):
                    MA7_S += list[j]

                LAG7_S = 0

                list = sales.index[(sales['date'] == sales['date'][i] - timedelta(7)) & (sales['store'] == sales['store'][i])].tolist()

                for j in range(len(list)):
                    LAG7_S += sales['quantity'][list[j]]

                result.loc[len(result)]=[sales['product'][i], sales['store'][i], (brand.index[product['brand'][sales['product'][i]] == brand['name']])[0],
                sales['date'][i], sales['quantity'][i], MA7_P, LAG7_P, sales_brand, MA7_B, LAG7_B, sales_store, MA7_S, LAG7_S]

    
    except pd._libs.tslibs.parsing.DateParseError:
        print("You entered wrong arguments! (2nd and 4th arguments are expected to be a datetime (YYYY-MM-DD))")
    except IndexError:
        print("Values caused an index error!")

result.to_csv('features.csv')

print(result)