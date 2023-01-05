import os
import netsuitefunctions
import time
import secrets
import requests
import xmltodict


config=netsuitefunctions.get_config()

timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
signature=netsuitefunctions.get_signature(config,timestamp,nonce)

operate_on="TimeBill"
schema="xmlns:tranEmp='urn:employees_2021_1.transactions.webservices.netsuite.com'"
stype=schema.split(":")[1].split("=")[0]
basic_type=f"{stype}:basic"
search_type=f'''{stype}:{operate_on}SearchAdvanced'''
search_id=216

soap= netsuitefunctions.get_soap(config,timestamp,signature,nonce,schema,search_type,search_id)
response = requests.post( url=config["url"], data=soap, headers=netsuitefunctions.get_headers())
dictionary = xmltodict.parse(response.text)
records = netsuitefunctions.get_records(dictionary)


Time_Bill_results=[]
for record in records:
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    data= netsuitefunctions.rename_key(data)
    if data["isBillable"]["searchValue"] != "false":
        Time_Bill_results.append(data)  
print(Time_Bill_results[0],"\n",Time_Bill_results[0].keys())




timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
signature=netsuitefunctions.get_signature(config,timestamp,nonce)
operate_on="Transaction"
schema="xmlns:tranSales='urn:sales_2021_1.transactions.webservices.netsuite.com'"
search_id=398
stype=schema.split(":")[1].split("=")[0]
basic_type=f"{stype}:basic"
search_type=f'''{stype}:{operate_on}SearchAdvanced'''



soap= netsuitefunctions.get_soap(config,timestamp,signature,nonce,schema,search_type,search_id)
response = requests.post( url=config["url"], data=soap, headers=netsuitefunctions.get_headers())
dictionary = xmltodict.parse(response.text)
records = netsuitefunctions.get_records(dictionary)


#print("\n\n\n\n")

Transaction_results=[]
for record in records:
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    data= netsuitefunctions.rename_key(data)
    #if data["status"]["searchValue"] != "paidInFull":
    Transaction_results.append(data)  
print(Transaction_results[0],"\n",Transaction_results[0].keys())


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