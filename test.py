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



NS_ACCOUNT='4455308_SB1'
NS_CONSUMER_KEY= '8fc8cb347b73302b89218daca19623c13ba8686fa0ad07cf406bd7da18aa31a7'
NS_CONSUMER_SECRET = 'c27755d1d7dd7386d73617a36055cd5a2a628ab513a752727ff340a6aa103ec8'
NS_TOKEN_KEY = '7cb4ae5c8c77161703802e96496b3d746425aa5e9fd979a9e3a1b76cf4da889f'
NS_TOKEN_SECRET = 'd1f978c443c8c597876bcb2c8dfb939ee3c4f85c1d5ee77f883a1286530a4116'
oauth_signature_method= 'HMAC-SHA256'
oauth_version = '1.0'
oauth_timestamp = str(int(time.time()))
oauth_nonce = ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=14))
oauth_signature_method= 'HMAC-SHA256'
url = "https://4455308-sb1.suitetalk.api.netsuite.com/services/NetSuitePort_2021_1"
timestamp: str = str(int(time.time()))
nonce: str = secrets.token_hex(14)
base_str: str = "&".join([NS_ACCOUNT, NS_CONSUMER_KEY, NS_TOKEN_KEY, nonce, timestamp])
key: str = "&".join([NS_CONSUMER_SECRET, NS_TOKEN_SECRET])
digest: bytes = hmac.new(str.encode(key), msg=str.encode(base_str), digestmod=hashlib.sha256).digest()
signature: str = base64.b64encode(digest).decode()


request_body =f'''<soapenv:Envelope
     xmlns:xsd='http://www.w3.org/2001/XMLSchema'
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:platformCore='urn:core_2021_1.platform.webservices.netsuite.com'
    xmlns:tranEmp='urn:employees_2021_1.transactions.webservices.netsuite.com'
    xmlns:platformMsgs='urn:messages_2021_1.platform.webservices.netsuite.com'>
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
            <searchRecord xsi:type='tranEmp:TimeSheetSearch'/>
        </search>
    </soapenv:Body>
</soapenv:Envelope>'''



#nonce for get = 20
#for search = 14

 


"""<soapenv:Envelope
    xmlns:xsd='http://www.w3.org/2001/XMLSchema'
    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
    xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/'
    xmlns:platformCore='urn:core_2021_1.platform.webservices.netsuite.com'
    xmlns:platformMsgs='urn:messages_2021_1.platform.webservices.netsuite.com'>
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
            <searchRecord xsi:type='tranEmp:TimeSheetSearch'/>
        </search>
    </soapenv:Body>
</soapenv:Envelope>"""

headers = {
            'Content-Type': 'application/json',
            #'prefer':'transient',
            'soapaction': 'search',
            #'Authorization': f'''OAuth realm="{self.NS_ACCOUNT}",oauth_consumer_key="{self.NS_CONSUMER_KEY}",oauth_token="{self.NS_TOKEN_KEY}",oauth_signature_method="{self.oauth_signature_method}",oauth_timestamp="{self.oauth_timestamp}",oauth_nonce="{self.oauth_nonce}",oauth_version="{self.oauth_version }",oauth_signature="{encoded_oauth_signature}"'''
            }

response = requests.post( url=url, data=request_body, headers=headers)
#print(response.content)
dictionary = xmltodict.parse(response.text)
#records= my_dict["soapenv:Envelope"]['soapenv:Body']['getResponse']['platformMsgs:readResponse']['platformMsgs:record']
String=""
String=get_string(String,dictionary,0)
print(String)
#for i in records:
#    print(i,":",records[i])
#json_data=json.load(my_dict)
#print(json_data)