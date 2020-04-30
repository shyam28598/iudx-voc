#!/usr/local/bin/python3
import json
import os
import glob
import sys

from collections import OrderedDict


classes_path = "../../bs-dm/classes/"
properties_path = "../../bs-dm/properties/"
expanded_path = "../../bs-dm/classes_expanded/"

#classes_path = sys.argv[1]
#properties_path = sys.argv[2]
#expanded_path = sys.argv[3]


def find(element, array):
    for item in array:
        if item['@id'] == element:
            return item


for class_file in glob.glob(os.path.join(classes_path, '*.jsonld')):
    domain = class_file.replace("../../bs-dm/classes/", "")
    domain = domain.replace(".jsonld", "")
    domain = "iudx:" + domain
    with open(class_file, "r+") as class_obj:
        new_dict = OrderedDict()
        obj = json.load(class_obj)
        if "@context" in obj.keys():
            new_dict["@context"] = obj["@context"]
            del(obj["@context"])
        else:
            print("@context missing in " + class_file)
        if "@graph" in obj.keys():
            new_dict["@graph"] = obj["@graph"]
            del(obj["@graph"])
        else:
            print("@graph missing in " + class_file)
        for prop_file in glob.glob(os.path.join(properties_path, '*.jsonld')):
            with open(prop_file, "r+") as prop_obj:
                prop = json.load(prop_obj)
                if "@graph" in prop.keys():
                    try:
                        includes = find(domain, prop["@graph"][0]["iudx:domainIncludes"])
                        if includes is not None:
                            new_dict["@graph"].append(prop["@graph"][0])
                    except KeyError:
                        print("iudx:domainIncludes not in " + prop_file)
                else:
                    print("@graph missing in " + prop_file)
        os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
        with open(expanded_path + domain.replace("iudx:", "") + ".jsonld", "w+") as new_file:
            json.dump(new_dict, new_file, indent=4)
