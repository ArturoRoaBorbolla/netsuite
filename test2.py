import oauth2 as oauth
import json
import requests
import time
import time #To generate the OAuth timestamp
import urllib.parse #To URLencode the parameter string
import hmac #To implement HMAC algorithm
import hashlib #To generate SHA256 digest
from base64 import b64encode #To encode binary data into Base64
import binascii #To convert data into ASCII
import requests #To make HTTP requests
import random
import time
from time import timezone
import base64
import secrets
import xmltodict
import collections
import re



def get_string(String,dictionary,level):
    for i in dictionary.keys():
        print(i)
        t=type(dictionary[i])
        print(t)
        if t is str:
            value=dictionary[i]
            if value != None and value != "":
                spaces = "\t" * level
                i=i.replace("_"," ")
                String += f"{spaces}{i} : {value}\n"
        elif t is dict or t is collections.OrderedDict:
            String=get_string(String,dictionary[i],level+1)
        elif t is list:
            for j in range(len(dictionary[i])):
                dictionary2=dictionary[i][j]
                String=get_string(String,dictionary2,level+1)
    return String


def replace_dic_name(data):
    my_dic={}
    print(type(data),data)
    if type(data) == dict:
        data.keys()
        for key in data.keys():
            if  re.search("^platform.*:", key) != None:
                print({ key.replace(re.search("^platform.*:", key).group(),"") : replace_dic_name(data[key])})
                my_dic.update({ key.replace(re.search("^platform.*:", key).group(),"") : replace_dic_name(data[key])})
            else:
                print({key : replace_dic_name(data[key])})
                my_dic.update({key : replace_dic_name(data[key])})
        return my_dic
    else:
        return data



def rename_key(dic):
    new_dic={}
    for key in dic.keys():
        if type(dic[key]) == str:
            if  re.search("^platform.*:", key) != None:
                new_dic[key.replace(re.search("^platform.*:", key).group(),"")] = dic[key]
            else:
                new_dic[key] = dic[key]
        elif type(dic[key]) == dict:
            if  re.search("^platform.*:", key) != None:
                new_dic[key.replace(re.search("^platform.*:", key).group(),"")]= rename_key(dic[key])
            else:
                new_dic[key] = dic[key]
        elif type(dic[key]) == list:
            list_of_elements=[]
            for element in dic[key]:
                another_dic={}
                for key2 in element.keys():
                    if type(element[key2]) == str:
                        if  re.search("^platform.*:", key2) != None:
                            another_dic[key2.replace(re.search("^platform.*:", key2).group(),"")] = element[key2]
                        else:
                            another_dic[key2] = element[key2]
                    elif type(element[key2]) == dict:
                        if  re.search("^platform.*:", key2) != None:
                            another_dic[key2.replace(re.search("^platform.*:", key2).group(),"")]= rename_key(element[key2])
                        else:
                            another_dic[key2] = element[key2]
                list_of_elements.append(another_dic) 
            if  re.search("^platform.*:", key) != None:
                return {key.replace(re.search("^platform.*:", key).group(),"") : list_of_elements}
            else:
                return {key : list_of_elements}
    return new_dic



NS_ACCOUNT='4455308_SB1'
NS_CONSUMER_KEY= '8fc8cb347b73302b89218daca19623c13ba8686fa0ad07cf406bd7da18aa31a7'
NS_CONSUMER_SECRET = 'c27755d1d7dd7386d73617a36055cd5a2a628ab513a752727ff340a6aa103ec8'
NS_TOKEN_KEY = '7cb4ae5c8c77161703802e96496b3d746425aa5e9fd979a9e3a1b76cf4da889f'
NS_TOKEN_SECRET = 'd1f978c443c8c597876bcb2c8dfb939ee3c4f85c1d5ee77f883a1286530a4116'
url = "https://4455308-sb1.suitetalk.api.netsuite.com/services/NetSuitePort_2021_1"
timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
base_str: str = "&".join([NS_ACCOUNT, NS_CONSUMER_KEY, NS_TOKEN_KEY, nonce, timestamp])
key: str = "&".join([NS_CONSUMER_SECRET, NS_TOKEN_SECRET])
digest: bytes = hmac.new(str.encode(key), msg=str.encode(base_str), digestmod=hashlib.sha256).digest()
signature: str = base64.b64encode(digest).decode()
data={}


operate_on="TimeBill"
operate_on="Transaction"


#schema="xmlns:tranEmp='urn:employees_2021_1.transactions.webservices.netsuite.com'"
schema="xmlns:tranSales='urn:sales_2021_1.transactions.webservices.netsuite.com'"

stype=schema.split(":")[1].split("=")[0]
basic_type=f"{stype}:basic"


search_type=f'''{stype}:{operate_on}SearchAdvanced'''

#search_id=216
search_id=398



request_body =f'''<soapenv:Envelope
     xmlns:xsd='http://www.w3.org/2001/XMLSchema'
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:platformCore='urn:core_2021_1.platform.webservices.netsuite.com'
    xmlns:platformMsgs='urn:messages_2021_1.platform.webservices.netsuite.com'
    {schema}>
    <soapenv:Header>
        <tokenPassport xsi:type='platformCore:TokenPassport'>
        <account  xsi:type='xsd:string'>{NS_ACCOUNT}</account>
        <consumerKey  xsi:type='xsd:string'>{NS_CONSUMER_KEY}</consumerKey>
        <token  xsi:type='xsd:string'>{NS_TOKEN_KEY}</token>
        <nonce  xsi:type='xsd:string'>{nonce}</nonce>
        <timestamp  xsi:type='xsd:long'>{timestamp}</timestamp>
        <signature algorithm='HMAC-SHA256' xsi:type='platformCore:TokenPassportSignature'>{signature}</signature>
        </tokenPassport>
    </soapenv:Header>
    <soapenv:Body>
        <search xsi:type='platformMsgs:SearchRequest'>
            <searchRecord xsi:type='{search_type}' savedSearchId='{search_id}'/>
        </search>
    </soapenv:Body>
</soapenv:Envelope>'''



headers = {
            'Content-Type': 'application/json',
            'soapaction': 'search',
            }

response = requests.post( url=url, data=request_body, headers=headers)
results=[]
dictionary = xmltodict.parse(response.text)
records=dictionary["soapenv:Envelope"]["soapenv:Body"]['searchResponse']['platformCore:searchResult']["platformCore:searchRowList"]["platformCore:searchRow"]
completed={}
for record in records:
    print("record")
    print(record)
    data_dict={}
    data = record[basic_type]
    data.pop("@xmlns:platformCommon")
    print("Renamed")
    data=rename_key(data)
    print(data)
    results.append(data)  
print(results)
   