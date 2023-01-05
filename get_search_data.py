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


results=[]
for record in records:
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    data= netsuitefunctions.rename_key(data)
    results.append(data)  
print(results)





