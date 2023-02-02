import os
import netsuitefunctions
import time
import secrets
import requests
import xmltodict
import numpy as np
from datetime import datetime


                  
                    
def get_id(data):
    if  type(data) is dict:
        #if data['@internalId'] == '103':
            return [data['searchValue']]
    if type(data) is list:
        sv=[]
        for i in data:
            #print(i['@internalId'])
            #if i['@internalId'] == '103':
                sv.append(i['searchValue'])
        return sv


def compare(Transaction_results,Time_Bill,counter,Output_Dict,number):
    for transaction in Transaction_results:
        try:
            invoice_from_transaction=transaction['tranId']['searchValue']
            #print(f"\t Document Number  {invoice_from_transaction}")
        except:
            pass
        else:
            #print(invoice_from_transaction,invoice_number_in_time)
            if invoice_from_transaction == number:
                #print(f"\t\tMatch {invoice_from_transaction} and {number}")
                dict_to_print = Time_Bill
                #print(f"Found {invoice_from_transaction}")
                dict_to_print.update(transaction)
                Output_Dict[counter]=dict_to_print
                counter +=1
    return counter



config=netsuitefunctions.get_config()

timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
signature=netsuitefunctions.get_signature(config,timestamp,nonce)

operate_on="TimeBill"
schema="xmlns:tranEmp='urn:employees_2021_1.transactions.webservices.netsuite.com'"
stype=schema.split(":")[1].split("=")[0]
basic_type=f"{stype}:basic"
criteria=f'''{stype}:{operate_on}Search'''
search_type=f'''{criteria}Advanced'''

#search_id=216
search_id=76

Time_from=f"2022-02-01"
Time_to=f"2023-03-01"
soap= netsuitefunctions.get_soap(config,timestamp,signature,nonce,schema,search_type,search_id,criteria,Time_from,Time_to)
print(soap)
response = requests.post( url=config["url"], data=soap, headers=netsuitefunctions.get_headers())
#print(response)
#print(response.text)
dictionary = xmltodict.parse(response.text)
records = netsuitefunctions.get_records(dictionary)


Time_Bill_results=[]
for record in records:
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    data= netsuitefunctions.rename_key(data)
    #if data["isBillable"]["searchValue"] != "false":
    Time_Bill_results.append(data)  
#print(Time_Bill_results[0],"\n",Time_Bill_results[0].keys())




timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
signature=netsuitefunctions.get_signature(config,timestamp,nonce)
operate_on="Transaction"
schema="xmlns:tranSales='urn:sales_2021_1.transactions.webservices.netsuite.com'"
stype=schema.split(":")[1].split("=")[0]
basic_type=f"{stype}:basic"
criteria=f'''{stype}:{operate_on}Search'''
search_type=f'''{criteria}Advanced'''
#search_id=398
search_id=437

Trans_from=f"2023-01-01"
Trans_to=f"2023-03-01"
soap= netsuitefunctions.get_soap(config,timestamp,signature,nonce,schema,search_type,search_id,criteria,Trans_from,Trans_to)
print(soap)
response = requests.post( url=config["url"], data=soap, headers=netsuitefunctions.get_headers())
#print(response.text)
dictionary = xmltodict.parse(response.text)
records = netsuitefunctions.get_records(dictionary)


#print("\n\n\n\n")

Transaction_results=[]
for record in records:
    #print(record)
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    data= netsuitefunctions.rename_key(data)
    #if data["status"]["searchValue"] != "paidInFull":
    Transaction_results.append(data)  
    #if "customFieldList" in data.keys():
    #    print(data)
#print(Transaction_results[0],"\n",Transaction_results[0].keys())

#invoice_number=Time_Bill_results[0]["customFieldList"]['customField']['searchValue']



print("Starting to try match data\n\n\n")
Output_Dict={}
counter=0
print(len(Time_Bill_results),len(Transaction_results))
for Time_Bill in Time_Bill_results:
    try:
        data=get_id(Time_Bill["customFieldList"]['customField'])
    except:
        pass
    else:
        for number in data:
            if type(number) is dict:
                number= number['@typeId']
                #print(f"Trying look for ID {number}")
                counter = compare(Transaction_results,Time_Bill,counter,Output_Dict,number)
            else:
                #print(f"Trying look for ID {number}")
                counter = compare(Transaction_results,Time_Bill,counter,Output_Dict,number)
print(Output_Dict)
            


#for time_bill in Time_Bill_results:
#    try:
#        invoice_number=time_bill["customFieldList"]['customField']['searchValue']
#    except:
#        pass
#    else:
#        for transaction in Transaction_results:
#            if 'customFieldList' in transaction.keys():
#                print(transaction['customFieldList']['customField'])
#                dt=get_id(transaction['customFieldList']['customField'])
#               if dt!=None:
#                    print(dt)
                    
  
'''        
for Transaction in Transaction_results:
    try:
        #print(Transaction["entity"]["searchValue"]["@internalId"])
        Customer = int(Transaction["entity"]["searchValue"]["@internalId"])
    except:
        pass
    else:
        for bill in Time_Bill_results:
            #print(Customer,bill["customer"]["searchValue"]["@internalId"])
            dict_to_print = Transaction
            if int(bill["customer"]["searchValue"]["@internalId"]) == Customer:
                dict_to_print.update(bill)
                print(dict_to_print)
                print("\n")
'''