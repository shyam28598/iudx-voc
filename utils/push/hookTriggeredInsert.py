"""
    This is a script for a github webhook to trigger.
    This script assumes that this script is not updated in the remote.
    If this script is updated, manually update the iudx-voc submodule in the voc-server.
    Give absolute paths to privkey and cert
"""

import json
import requests
import os
import sys
import time

# Wait for repo to get updated
time.sleep(5)

# Generate classes
os.system("python3 utils/generation/generate_class.py")
# Generate master context
os.system("python3 utils/generation/generate_master.py")

# Wait for schemas to get generated
time.sleep(5)



cert_file = "keys/cert.pem"
key_file = "keys/private-key.pem"


all_classes_folder = "/tmp/generated_classes/"
all_properties_folder = "/tmp/all_properties/"
master_context_file = "./iudx.jsonld"

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

with open(master_context_file, "r") as f:
    master_context = json.load(f)
    print("Pushing master context")
    r = requests.post(url, data=json.dumps(master_context), headers=voc_headers)
    print(r.status_code)
    if r.status_code != 201:
        print("Failed")


with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
