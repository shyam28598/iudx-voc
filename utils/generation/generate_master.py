import json
import os
from collections import OrderedDict

classes_folder = "./base-schemas/classes/"
dm_classes_folder = "./data-models/classes"
properties_folder = "./base-schemas/properties/"
dm_properties_folder = "./data-models/properties/"
types_folder = "./data-types/classes/"

folders = [classes_folder, dm_classes_folder,
            properties_folder, dm_properties_folder, types_folder]

output_file = "iudx.jsonld"


context = OrderedDict()
contextsources = {}
context = {}

contextsources["type"] = "@type"
contextsources["id"] = "@id"
contextsources["@vocab"] = "https://voc.iudx.org.in/"

for fldr in folders:
    for fl in os.listdir(fldr):
        with open(os.path.join(fldr, fl), "r") as f:
            try:
                schema = json.load(f)
                contextsources = {**contextsources,
                                  **schema["@context"]}
                context = {**context,
                           **{fl[:-7]: {"@id": "iudx:"+fl[:-7]}}}
            except Exception as e:
                print("Class - " + fl[:-7] + " failed")
                print(e)



context = {**contextsources, **context}
context_output = {"@context": context}

with open(output_file, "w") as f:
    json.dump(context_output, f, indent=4)
