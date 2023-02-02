import oauth2 as oauth
import json
import base64
import re
import hmac
import os
import hashlib
from datetime import datetime

directory_path = os.path.dirname(os.path.realpath(__file__)) 


def create_Transaction_criteria(stype,Trans_from,Trans_to):
    #year=int(datetime.now().strftime("%Y")) - 1 
    ##month=int(datetime.now().strftime("%m")) - 1
    #if len(str(month)) < 2:
    #    month = f"0{month}" 
    #day=int(datetime.now().strftime("%d"))
    #if len(str(day)) < 2:
    #    day = f"0{day}" 
    if "EMP" in stype.upper():
        op="date"
        search="TimeBill"
    else:
        op="tranDate"
        search="Transaction"
    return f'''    <criteria xsi:type='{stype}'>
                    <basic xsi:type='platformCommon:{search}SearchBasic'>
                        <{op} operator='within' xsi:type='platformCore:SearchDateField'>
                            <searchValue xsi:type='xsd:dateTime'>{Trans_from}T07:14:11.783Z</searchValue>
                            <searchValue2 xsi:type='xsd:dateTime'>{Trans_to}T07:14:11.783Z</searchValue2>
                        </{op}>
                    </basic>
                </criteria>'''

def get_config():
    config=json.loads(open(f"{directory_path}\\config.ini").read())
    NS_ACCOUNT = base64.b64decode(config["NS_ACCOUNT"]).decode("utf-8")
    NS_CONSUMER_KEY = base64.b64decode(config["NS_CONSUMER_KEY"]).decode("utf-8")
    NS_CONSUMER_SECRET=base64.b64decode(config["NS_CONSUMER_SECRET"]).decode("utf-8")
    NS_TOKEN_KEY= base64.b64decode(config["NS_TOKEN_KEY"]).decode("utf-8")
    NS_TOKEN_SECRET = base64.b64decode(config["NS_TOKEN_SECRET"]).decode("utf-8")
    url= base64.b64decode(config["url"]).decode("utf-8")
    return {
    "NS_ACCOUNT" : NS_ACCOUNT, 
    "NS_CONSUMER_KEY" :  NS_CONSUMER_KEY,
    "NS_CONSUMER_SECRET" : NS_CONSUMER_SECRET,
    "NS_TOKEN_KEY" : NS_TOKEN_KEY,
    "NS_TOKEN_SECRET" : NS_TOKEN_SECRET,
    "url" : url,
    }


def get_signature(config,timestamp,nonce):
    base_str: str = "&".join([config["NS_ACCOUNT"], config["NS_CONSUMER_KEY"], config["NS_TOKEN_KEY"], nonce, timestamp])
    key: str = "&".join([config["NS_CONSUMER_SECRET"], config["NS_TOKEN_SECRET"]])
    digest: bytes = hmac.new(str.encode(key), msg=str.encode(base_str), digestmod=hashlib.sha256).digest()
    signature: str = base64.b64encode(digest).decode()
    return signature

def get_soap(config,timestamp,signature,nonce,schema,search_type,search_id,stype,Trans_from,Trans_to):
    Transcriteria= create_Transaction_criteria(stype,Trans_from,Trans_to)
    return f'''<soapenv:Envelope
     xmlns:xsd='http://www.w3.org/2001/XMLSchema'
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:platformCore='urn:core_2021_1.platform.webservices.netsuite.com'
    xmlns:platformCommon='urn:common_2021_1.platform.webservices.netsuite.com'
    xmlns:platformMsgs='urn:messages_2021_1.platform.webservices.netsuite.com'
    {schema}>
    <soapenv:Header>
        <tokenPassport xsi:type='platformCore:TokenPassport'>
        <account  xsi:type='xsd:string'>{config["NS_ACCOUNT"]}</account>
        <consumerKey  xsi:type='xsd:string'>{config["NS_CONSUMER_KEY"]}</consumerKey>
        <token  xsi:type='xsd:string'>{config["NS_TOKEN_KEY"]}</token>
        <nonce  xsi:type='xsd:string'>{nonce}</nonce>
        <timestamp  xsi:type='xsd:long'>{timestamp}</timestamp>
        <signature algorithm='HMAC-SHA256' xsi:type='platformCore:TokenPassportSignature'>{signature}</signature>
        </tokenPassport>
    </soapenv:Header>
    <soapenv:Body>
        <search xsi:type='platformMsgs:SearchRequest'>
            <searchRecord xsi:type='{search_type}' savedSearchId='{search_id}'>
            {Transcriteria}
            </searchRecord>
        </search>
    </soapenv:Body>
</soapenv:Envelope>'''


def get_headers():
    return {
            'Content-Type': 'application/json',
            'soapaction': 'search',
            }

def get_records(response_dict):
    return response_dict["soapenv:Envelope"]["soapenv:Body"]['searchResponse']['platformCore:searchResult']["platformCore:searchRowList"]["platformCore:searchRow"]


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
