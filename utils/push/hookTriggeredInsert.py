"""
    This is a script for a github webhook to trigger.
    Give absolute paths to privkey and cert
"""

import json
import requests
import os
import sys


os.system("git pull origin master")
os.system("python utils/generation/generate_class.py")


cert_file = "keys/cert.pem"
key_file = "keys/private-key.pem"


all_classes_folder = "/tmp/generated_classes/"
all_properties_folder = "/tmp/all_properties/"

folders = [all_classes_folder, all_properties_folder]


cert = (cert_file, key_file)
auth_api = "https://auth.iudx.org.in/auth/v1/token"
auth_headers = {"content-type": "application/json"}
payload = { "request" : [ {"id": "datakaveri.org/f7e044eee8122b5c87dce6e7ad64f3266afa41dc/voc.iudx.org.in/*"} ] }

url = "https://voc.iudx.org.in"



# Obtain token from auth server
token = requests.post(auth_api, data=json.dumps(payload),
                        headers=auth_headers, cert=cert).json()["token"]

voc_headers = {"token": token, "content-type": "application/ld+json", "accept": "application/ld+json"}
print(voc_headers)



failed_list = []


for fldr in folders:
    for filename in os.listdir(fldr):
        with open(fldr + "/" + filename, 'r') as f:
            doc = json.load(f)
            name = doc["@graph"][0]["@id"][5:]
            print("Pushing " + name)
            r = requests.post(url+"/"+name, data=json.dumps(doc), headers=voc_headers)
            if r.status_code != 201 :
                failed_list.append(name)



with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
