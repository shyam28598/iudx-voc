"""
    This is a script triggered by github webhook to insert schemas into the voc-server.
    Give relative paths to privkey and cert from iudx-voc folder
"""

import json
import requests
import os
import sys
import time

cert_file = "keys/cert.pem"
key_file = "keys/private-key.pem"


all_classes_folder = "/tmp/generated_classes/"
all_properties_folder = "/tmp/all_properties/"
all_examples_folder = "/tmp/all_examples/"
master_context_file = "./iudx.jsonld"

schema_folders = [all_classes_folder, all_properties_folder]


cert = (cert_file, key_file)
auth_api = "https://authdev.iudx.io/auth/v1/token"
auth_headers = {"content-type": "application/json"}
payload = { "request" : [ {"id": "datakaveri.org/f7e044eee8122b5c87dce6e7ad64f3266afa41dc/voc.iudx.org.in/*"} ] }

url = "https://voc.iudx.org.in/"



# Obtain token from auth server
token = requests.post(auth_api, data=json.dumps(payload),
                        headers=auth_headers, cert=cert).json()["token"]

voc_headers = {"token": token, "content-type": "application/ld+json", "accept": "application/ld+json"}



failed_list = []

failed_schemas = []
failed_examples = []


def post_schema(name, path, doc, max_retries=5):

    if max_retries > 0:
        try:
            r = requests.post(url+path+name, data=json.dumps(doc), 
                    headers=voc_headers, timeout=3)
            if r.status_code != 201:
                post_schema(name, path, doc, max_retries=max_retries-1)
            else:
                return 1
        except Exception as e:
            post_schema(name, path, doc, max_retries=max_retries-1)
        return 1
    return 0


for fldr in schema_folders:
    for filename in os.listdir(fldr):
        try:
            with open(fldr + "/" + filename, 'r') as f:
                print("Pushing " + filename)
                doc = json.load(f)
                name = doc["@graph"][0]["@id"][5:]
                status = post_schema(name, "", doc)
                if (status == 0):
                    failed_list.append(name)
        except Exception as e:
            print("Failed inserting " + name)
            failed_list.append(name)
            failed_schemas.append("fldr" + "/" + filename)

for filename in os.listdir(all_examples_folder):
    try:
        with open(all_examples_folder + "/" + filename, 'r') as f:
            print("Pushing " + filename)
            doc = json.load(f)
            status = post_schema(filename, "examples/", doc)
            if status == 0 :
                failed_list.append(filename)
    except Exception as e:
        print("Failed inserting " + filename)
        failed_list.append(filename)

with open(master_context_file, "r") as f:
    master_context = json.load(f)
    print("Pushing master context")
    status = post_schema("", "", master_context)
    if status == 0:
        failed_list.append("master")

print( "Failed inserting - ", failed_list)
with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
