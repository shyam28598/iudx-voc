#!/usr/local/bin/python3

import json
import os,glob

folder_path = "../base-schemas/classes/"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
        for field in obj["@graph"]:
            label = field["@id"].split(":")
            tmp = field["rdfs:label"]
            field["rdfs:label"] = label[1]

        obj_file.seek(0)
        json.dump(obj, obj_file, indent=4)
        obj_file.truncate()
