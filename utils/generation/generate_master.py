import json
import os
from collections import OrderedDict

classes_folder = "./base-schemas/classes/"
properties_folder = "./base-schemas/properties/"
datamodel_classes_folder = ""
datamodel_properties_folder = ""

output_file = "iudx.jsonld"


context = OrderedDict()
contextsources = {}
context = {}

contextsources["type"] = "@type"
contextsources["id"] = "@id"
contextsources["@vocab"] = "http://voc.iudx.org.in/"

""" Classes """
for fl in os.listdir(classes_folder):
    with open(os.path.join(classes_folder, fl), "r") as f:
        try:
            schema = json.load(f)
            contextsources = {**contextsources,
                              **schema["@context"]}
            context = {**context,
                       **{fl[:-7]: {"@id": "iudx:"+fl[:-7]}}}
        except Exception as e:
            print("Class - " + fl[:-7] + " failed")
            print(e)


""" Properties """
for fl in os.listdir(properties_folder):
    with open(os.path.join(properties_folder, fl), "r") as f:
        try:
            schema = json.load(f)
            contextsources = {**contextsources,
                              **schema["@context"]}
            context = {**context,
                       **{fl[:-7]: {"@id": "iudx:"+fl[:-7]}}}
        except Exception as e:
            print("Property - " + fl[:-7] + " failed")
            print(e)

context = {**contextsources, **context}
with open(output_file, "w") as f:
    json.dump(context, f, indent=4)
