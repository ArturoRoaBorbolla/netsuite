import os
import base64
import json

directory_path = os.path.dirname(os.path.realpath(__file__)) 

with open(f"{directory_path}\\config.txt") as text_file:
    vars=text_file.readlines()
ini={}
for var in vars:
    key_value=var.split("=")
    #print(key_value)
    key = key_value[0]
    value= base64.b64encode(key_value[1].strip().encode()).decode()
    ini.update({key:value})
with open(f"{directory_path}\\config.ini","w") as ini_file:
    ini_file.write(json.dumps(ini))
     
    
