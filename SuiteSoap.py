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

NS_ACCOUNT='4455308_SB1'
NS_CONSUMER_KEY= '8fc8cb347b73302b89218daca19623c13ba8686fa0ad07cf406bd7da18aa31a7'
NS_CONSUMER_SECRET = 'c27755d1d7dd7386d73617a36055cd5a2a628ab513a752727ff340a6aa103ec8'
NS_TOKEN_KEY = '7cb4ae5c8c77161703802e96496b3d746425aa5e9fd979a9e3a1b76cf4da889f'
NS_TOKEN_SECRET = 'd1f978c443c8c597876bcb2c8dfb939ee3c4f85c1d5ee77f883a1286530a4116'
oauth_signature_method= 'HMAC-SHA256'
oauth_version = '1.0'
oauth_timestamp = str(int(time.time()))
oauth_nonce1 = ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=11))
oauth_signature_method= 'HMAC-SHA256'
oauth_nonce2 = ''.join(random.choices("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20))

class SuiteSearch:
    def init_signature(self,NS_ACCOUNT,NS_CONSUMER_KEY,NS_CONSUMER_SECRET,NS_TOKEN_KEY,NS_TOKEN_SECRET,oauth_signature_method,oauth_version,oauth_timestamp,oauth_nonce):
        self.NS_ACCOUNT = NS_ACCOUNT
        self.NS_CONSUMER_KEY = NS_CONSUMER_KEY 
        self.NS_CONSUMER_SECRET = NS_CONSUMER_SECRET
        self.NS_TOKEN_KEY = NS_TOKEN_KEY
        self.NS_TOKEN_SECRET= NS_TOKEN_SECRET
        self.oauth_signature_method = oauth_signature_method
        self.oauth_version = oauth_version 
        self.oauth_timestamp = oauth_timestamp
        self.oauth_nonce = oauth_nonce2
        self.signing_key =  NS_CONSUMER_SECRET + '&' + NS_TOKEN_SECRET
        self.parameter_string = ''
        self.method = 'POST'
        self.json={}

    def create_parameter_string(self):
        self.parameter_string = self.parameter_string + 'oauth_consumer_key=' + self.NS_CONSUMER_KEY
        self.parameter_string = self.parameter_string + '&oauth_nonce=' + self.oauth_nonce
        self.parameter_string = self.parameter_string + '&oauth_signature_method=' + self.oauth_signature_method
        self.parameter_string = self.parameter_string + '&oauth_timestamp=' + self.oauth_timestamp
        self.parameter_string = self.parameter_string + '&oauth_token=' + self.NS_TOKEN_KEY
        self.parameter_string = self.parameter_string + '&oauth_version=' + self.oauth_version
        self.parameter_string

    def create_signature(self,secret_key, signature_base_string):
        self.encoded_string = signature_base_string.encode()
        self.encoded_key = secret_key.encode()
        self.temp = hmac.new(self.encoded_key, self.encoded_string, hashlib.sha256).hexdigest()
        self.byte_array = b64encode(binascii.unhexlify(self.temp))
        return self.byte_array.decode()
    
    def get_soap(self,signature,searchid,nonce,time):
        return f'''
        <soapenv:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
        xmlns:platformCore="urn:core_2021_1.platform.webservices.netsuite.com" 
        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
        xmlns:platformMsgs="urn:messages_2021_1.platform.webservices.netsuite.com" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <soapenv:Body>
        <get xsi:type="platformMsgs:GetRequest">
            <baseRef type="employee" internalId="3156" xsi:type="platformCore:RecordRef"/>
        </get>
    </soapenv:Body>
</soapenv:Envelope>'''

        

    def execute(self):
        self.init_signature(NS_ACCOUNT=NS_ACCOUNT,NS_CONSUMER_KEY=NS_CONSUMER_KEY,NS_CONSUMER_SECRET=NS_CONSUMER_SECRET,NS_TOKEN_KEY=NS_TOKEN_KEY,NS_TOKEN_SECRET=NS_TOKEN_SECRET,oauth_signature_method=oauth_signature_method,oauth_version = oauth_version,oauth_timestamp = oauth_timestamp ,oauth_nonce = oauth_nonce2)
        self.create_parameter_string()
        self.encoded_parameter_string = urllib.parse.quote(self.parameter_string, safe='')
        url = "https://4455308-sb1.suitetalk.api.netsuite.com/services/NetSuitePort_2021_1"
        encoded_base_string = self.method + '&' + urllib.parse.quote(url, safe='')
        encoded_base_string = encoded_base_string + '&' + self.encoded_parameter_string
        oauth_signature = self.create_signature(self.signing_key, encoded_base_string)
        encoded_oauth_signature = urllib.parse.quote(oauth_signature, safe='')
        headers = {
            'Content-Type': 'text/xml',
            #'prefer':'transient',
            'soapaction': 'get',
            #'Authorization': f'''OAuth realm="{self.NS_ACCOUNT}",oauth_consumer_key="{self.NS_CONSUMER_KEY}",oauth_token="{self.NS_TOKEN_KEY}",oauth_signature_method="{self.oauth_signature_method}",oauth_timestamp="{self.oauth_timestamp}",oauth_nonce="{self.oauth_nonce}",oauth_version="{self.oauth_version }",oauth_signature="{encoded_oauth_signature}"'''
            }

        soap=self.get_soap(encoded_oauth_signature,96,oauth_nonce2,str(int(time.time())))
        print(soap)
        time.sleep(3)
        response = requests.post(url, data=soap,headers=headers)
        #self.json = json.loads(response.text)
        #return self.json
        print(response.text)
        #time.sleep(3)
        