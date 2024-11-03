a = """
Commands:
viewitems
add <icode> <cat> <name> <istock> <iprice> <discount>
remove <icode>
stock <icode> <change>
edit <icode> <field> <value>
newbill
viewsales
viewlastbill
savedb
exit

bill commands:
cancel
addedit <icode> <qty>
remove <icode> <qty>

use \"-\" instead of spaces in between of entries
"""
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import os

fields = ['icode','category','name','istock','iprice',"idiscount","isold"]
store = pd.read_csv("./data/db.csv", header=None, index_col=0, names=['icode','category','name','istock','iprice',"idiscount","isold","netsales"], dtype={"istock":int,"iprice":float,"idiscount":float,"isold":float,"netsales":float})
last_bill = pd.read_csv("./data/lastbill.csv", header=None, index_col=0, names=['name','qty','price',"discount","amt"])

def parse_bill(inp: str):
    y = inp.strip().split(" ")
    y[1] = y[1].upper()
    if y[0].upper() == "ADDEDIT":
        try:
            aoe_bill(y[1],int(y[2]))
        except  IndexError:
            print("Invalid input")
        
    elif y[0].upper() == "REMOVE":
        try:
            rem_bill_item(y[1])
        except AttributeError:
            print("Item not in bill")

    else:
        print("Invalid command")
        
def parse_menu(inp: str):
    x = inp.strip().split(" ")
    try:
        x[1] = x[1].upper()
    except:
        pass
    if x[0].upper() == "EXPORT":
        export_data(store)
    elif x[0].upper() == "ADD":
        add_item(x[1],x[2].replace("-"," "),x[3].replace("-"," "),int(x[4]),float(x[5]),float(x[6]),int(x[7]),int(x[8]))
        print("New Item added!")
    elif x[0].upper() == "REMOVE":
        rem_item(x[1])
        print("Item removed!")
    elif x[0].upper() == "STOCK":
        stock(x[1],int(x[2]))
        print("Stock updated!")
    elif x[0].upper() == "EDIT":
        edit(x[1],x[2],x[3].replace("-"," "))
        print("Data edited!")
    elif x[0].upper() == "HELP":
        print(a)
    elif x[0].upper() == "VIEWITEMS":
        print(store)
    elif x[0].upper() == "NEWBILL":
        makebill()
    elif x[0].upper() == "CLS":
        os.system("cls")
    elif x[0].upper() == "EXIT":
        z = input("Do you want to save changes? (y/n): ")
        if z == "y":
            export_data(store)
            exit()
        else:
            exit()
    elif x[0].upper() == "SAVEDB":
        export_data(store)
    elif x[0].upper() == "VIEWSALES":
        viewsales()
    elif x[0].upper() == "VIEWLASTBILL":
        print(last_bill)
    else:
        print("no such command as", x[0], "try \"help\"")
        
def main():
    global store
    print("Welcome to CheckOutApp")
    print("Type \"help\" to get to list of all commands")
    
    while True:
        inx = input("> ")
        try:
            parse_menu(inx)
        except IndexError:
             print("Missing Arguments, use \"help\"")


#db commands

def stock(icode: str,change:int):
    if store.loc[icode,"istock"]+change >= 0:
        store.loc[icode,'istock'] += change
    else:
        print("Must have atleast 0 stock")
    
def edit(icode: int, field: str ,value: any):
    store.loc[icode,field]=value

def add_item(icode: str,cat: str,name: str,istock: int,iprice: float,discount: float,isold: int, netsales: float):
    store.loc[icode]=[cat,name,istock,iprice,discount,isold, netsales]

def rem_item(icode: str):
    del store.loc[icode]

def export_data(df:pd.DataFrame):
    df.to_csv("./data/db.csv",header=False, index_label="icode")

#bill commands

def aoe_bill(icode: str,qty: int): # add if not present/ edit if present
    global bill
    if store.loc[icode,"istock"] >= qty:
        bill.loc[icode] = [store.loc[icode,'name'],qty,store.loc[icode,'iprice'],store.loc[icode,'idiscount'],0]
        bill.loc[icode,'amt'] = store.loc[icode,'iprice']*qty*(100-store.loc[icode,'idiscount'])/100
    else: 
        print("\n")
        print("Not enough stock")
    print("\n")
    print(bill)
    print('\n')    

def rem_bill_item(icode):
    try:
        del bill.loc[icode]
    except:
        print("Item not in bill")
    print("\n")
    print(bill)
    print('\n')
    
def finalize_bill():
    global now
    print("Bill finalized")
    now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Timestamp: ",now)
    print("Customer Name: ", cname)
    print("Total Amount: ",bill['amt'].sum())
    print(bill)
    for i in bill.index:
        store.loc[i,"istock"] -= bill.loc[i,'qty']
        store.loc[i,"isold"] += bill.loc[i,'qty']
        store.loc[i,"netsales"] += bill.loc[i,'amt']
    bill.to_csv('./data/lastbill.csv',index_label=cname+" "+now,header=False)


def makebill():
    global bill
    bill = pd.DataFrame(columns=['name','qty','price',"discount","amt"])
    global cname
    print(store)
    print("Ready for bill generation")
    cname = input("Enter customer name: ")
    while True:
        iny = input(">bill>")
        if iny.upper() == "CANCEL":
            break
        elif iny.upper() == "FINALIZE":
            finalize_bill()
            break 
        parse_bill(iny)


def viewsales():
    plt.figure(figsize=(10,6))
    plt.subplot(1, 2, 1)
    plt.bar(store.index,store['isold'])
    plt.title("Units sold")
    plt.subplot(1, 2, 2)
    plt.barh(store.index,store['netsales']//1000)
    plt.title("Sales in thousands")
    plt.tight_layout()
    plt.show()
main()