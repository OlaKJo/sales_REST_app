# init_db.py
import sqlite3
import pandas as pd
from pathlib import Path

# In order for the following to work you must have the data files on hand and in the data directory

sqliteConnection = sqlite3.connect('../data/sales.db')
sqliteCursor = sqliteConnection.cursor()

# Drop tables if there are tables which these names present
sqliteCursor.execute('''DROP TABLE IF EXISTS sales''')
sqliteCursor.execute('''DROP TABLE IF EXISTS store_cities''')
sqliteCursor.execute('''DROP TABLE IF EXISTS product_hierarchy''')

# Create the appropriate tables with schemas as defined below
sqliteCursor.execute('''CREATE TABLE IF NOT EXISTS sales (product_id,store_id,date,sales,revenue,stock,price,promo_type_1,promo_bin_1,promo_type_2,promo_bin_2,promo_discount_2,promo_discount_type_2)''')
sqliteCursor.execute('''CREATE TABLE IF NOT EXISTS store_cities (store_id,storetype_id,store_size,city_id)''')
sqliteCursor.execute('''CREATE TABLE IF NOT EXISTS product_hierarchy (product_id,product_length,product_depth,product_width,cluster_id,hierarchy1_id,hierarchy2_id,hierarchy3_id,hierarchy4_id,hierarchy5_id)''')

# load the data into a Pandas DataFrame
salesData = pd.read_csv('sales.csv/sales.csv')
prodData = pd.read_csv('product_hierarchy.csv');
storeData = pd.read_csv('store_cities.csv');

# write the data to sqlite tables in the db
salesData.to_sql('sales', sqliteConnection, if_exists='append', index = False)
prodData.to_sql('product_hierarchy', sqliteConnection, if_exists='append', index = False)
storeData.to_sql('store_cities', sqliteConnection, if_exists='append', index = False)
