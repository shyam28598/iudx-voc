#! /usr/local/bin/python3

import csv
import json
import copy
import os
from collections import OrderedDict

template_file = "./template.jsonld"

csv_file_path = [
                "./Device - Device_properties.csv"]
#                "./Environment - EnvAQM_properties.csv", "./Environment - EnvFlood_properties.csv", ]
#                "./Civic - WifiHotspot_properties.csv", "./Civic - StreetLightFeeder_properties.csv"]
#ignore = ["Custom", "location", "deviceModel", "rainfallMeasured", "rainfallForecast", "name", ""]

if not os.path.exists("./properties/"):
    os.makedirs("./properties/")
properties_path = "./Properties/"



def gen_properties(file_path):
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = data[1:]
        for item in data:
            if item[7] == "0":
                csv_label = item[0]
                csv_type = item[1]
                csv_comment = item[2]
                csv_domain = item[3]
                csv_range = item[4]
                csv_match = item[5]
                if "," in csv_domain:
                    csv_domain_list = csv_domain.split(",")
                else:
                    tmp_domain_list = []
                    tmp_domain_list.append(csv_domain)
                    csv_domain_list = tmp_domain_list
                if "," in csv_range:
                    csv_range_list = csv_range.split(",")
                else:
                    tmp_range_list = []
                    tmp_range_list.append(csv_range)
                    csv_range_list = tmp_range_list
                with open(template_file, "r") as template:
                    new_dict = OrderedDict()
                    obj = json.load(template)
                    if "@context" in obj.keys():
                        new_dict["@context"] = obj["@context"]
                        del(obj["@context"]) 
                    else:
                        print("@context missing in  "+ csv_label)
                    if "@graph" in obj.keys():
                        new_list = []
                        tmp_obj = OrderedDict()
                        new_list.append(tmp_obj)
                        tmp_obj["@id"] = "iudx:" + csv_label
                        if csv_type == "QP":
                            prop_list = []
                            prop_list.append("iudx:QuantitativeProperty")
                            tmp_obj["@type"] = prop_list
                        elif csv_type == "TP":
                            prop_list = []
                            prop_list.append("iudx:TimeProperty")
                            tmp_obj["@type"] = prop_list
                        elif csv_type == "TXP":
                            prop_list = []
                            prop_list.append("iudx:TextProperty")
                            tmp_obj["@type"] = prop_list
                        elif csv_type == "SP":
                            prop_list = []
                            prop_list.append("iudx:StructuredProperty")
                            tmp_obj["@type"] = prop_list
                        elif csv_type == "GP":
                            prop_list = []
                            prop_list.append("iudx:GeoProperty")
                            tmp_obj["@type"] = prop_list
                        tmp_obj["rdfs:comment"] = csv_comment
                        tmp_obj["rdfs:label"] = csv_label
                        tmp_obj["rdfs:isDefinedBy"] = obj["@graph"][0]["rdfs:isDefinedBy"]
                        try:
                            domain_list = []
                            for item in csv_domain_list:
                                domain_dict = {}
                                if ":" in item:
                                    domain_dict["@id"] = item.strip()
                                else:
                                    domain_dict["@id"] = "iudx:" + item.strip()
                                domain_list.append(domain_dict)
                        except NameError:
                            domain_list = []
                            domain_dict = {}
                            if ":" in csv_domain:
                                domain_dict["@id"] = csv_domain.strip()
                            else:
                                domain_dict["@id"] = "iudx:" + csv_domain.strip()
                            domain_list.append(domain_dict)
                        tmp_obj["iudx:domainIncludes"] = domain_list
                        try:
                            range_list = []
                            for item in csv_range_list:
                                range_dict = {}
                                range_dict["@id"] = "iudx:" + item.strip()
                                range_list.append(range_dict)
                        except NameError:
                            range_list = []
                            range_dict = {}
                            range_dict["@id"] = "iudx:" + csv_range.strip()
                            range_list.append(range_dict)
                        tmp_obj["iudx:rangeIncludes"] = range_list
                        if csv_match:
                            match_dict = {}
                            match_dict["@id"] = csv_match
                            tmp_obj["skos:exactMatch"] = match_dict
                        new_dict["@graph"] = new_list
                        with open(properties_path + csv_label + ".jsonld", "w+") as prop_file:
                            json.dump(new_dict, prop_file, indent=4)
                    else:
                        print("@graph missing in  "+ csv_label)


for path in csv_file_path:
    gen_properties(path)
