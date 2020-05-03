#! /usr/local/bin/python3

import csv
import json
import copy
import os
from collections import OrderedDict

qp_path = "./baseQP.jsonld"
tp_path = "./baseTxP.jsonld"

csv_file_path = "./DataModel_Properties - EnvAQM_properties.csv"
ignore = ["Custom", "location", "deviceModelInfo", ""]

if not os.path.exists("../../../data-models/properties/"):
    os.makedirs("../../../data-models/properties/")
properties_path = "../../../data-models/properties/"


def gen_properties(base_property):
    with open(base_property, "r") as qp_file:
        new_dict = OrderedDict()
        obj = json.load(qp_file)
        if "@context" in obj.keys():
            new_dict["@context"] = obj["@context"]
            del(obj["@context"]) 
        else:
            print("@context missing in  + filename")
        if "@graph" in obj.keys():
            new_list = []
            tmp_obj = OrderedDict()
            new_list.append(tmp_obj)
            obj["@graph"][0]["rdfs:label"] = csv_label
            obj_id = obj["@graph"][0]["@id"].split(":")
            obj_id[1] = csv_label
            tmp_id = ":"
            tmp_id = tmp_id.join(obj_id)
            obj["@graph"][0]["@id"] = tmp_id 
            obj["@graph"][0]["rdfs:comment"] = csv_comment
            tmp_obj["@id"] = obj["@graph"][0]["@id"]
            tmp_obj["@type"] = obj["@graph"][0]["@type"]
            tmp_obj["rdfs:label"] = obj["@graph"][0]["rdfs:label"]
            tmp_obj["rdfs:comment"] = obj["@graph"][0]["rdfs:comment"]
            tmp_obj["iudx:domainIncludes"] = obj["@graph"][0]["iudx:domainIncludes"]
            tmp_obj["iudx:rangeIncludes"] = obj["@graph"][0]["iudx:rangeIncludes"]
            new_dict["@graph"] = new_list
            with open(properties_path + csv_label + ".jsonld", "w+") as prop_file:
                json.dump(new_dict, prop_file, indent=4)
        else:
            print("@graph missing in  + filename")


with open(csv_file_path, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
    data = data[1:]
    for item in data:
        if item[0] not in ignore:
            csv_label = item[0]
            csv_type = item[1]
            csv_comment = item[2]
            if "QP" in csv_type:
                gen_properties(qp_path)
            elif "TXP" in csv_type:
                gen_properties(qp_path)
