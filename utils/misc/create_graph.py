#!/usr/local/bin/python3
import json
import os
import glob
import copy

from collections import OrderedDict


folder_path = "../../base-schemas/properties/"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
        if "@graph" not in obj.keys():
            new_dict = OrderedDict()
            new_list = []
            template = copy.deepcopy(obj)
            del(obj["@context"]) 
            new_list.append(copy.deepcopy(obj))
            new_dict["@context"] = template["@context"]
            new_dict["@graph"] = new_list
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()
        else:
            print("Graph already present in " + filename)
