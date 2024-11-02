"""
Category coding:

"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def import_data():
    return pd.read_csv("./data/db.csv", header=None, index_col=0, names=['icode','category','name','istock','iprice',"idiscount"])

def add_item(icode,cat,name,istock,iprice,discount):
    store.loc[icode]=[cat,name,istock,iprice,discount]

def export_data(df:pd.DataFrame):
    df.to_csv("./data/db.csv",header=False, index_label="icode")

store = import_data()

# add_item("FUR10001798","Furniture","Bush Somerset Collection Bookcase",2,261.96,0)
# add_item("OFF10002365","Office Supplies","Xerox 1967",15.552,3,0.2)
add_item("TEC10001949","Technology","Cisco SPA 501G IP Phone",213.48,3,0.2)
print(store)
export_data(store)