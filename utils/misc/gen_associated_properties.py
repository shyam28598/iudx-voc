#!/usr/local/bin/python3
import json
import os
import glob

from collections import OrderedDict


folder_path = "../../base-schemas/classes_expanded/"

with open("iudx-voc-properties.txt", "w+") as text_file:
    def get_class(name, cls):
        print(cls + "- " + name, file=text_file)
    
    
    def get_property(name):
        print("Property- " + name, file=text_file)
    
    
    def graph(obj):
        if "@graph" in obj.keys():
            for i in obj["@graph"]:
                if isinstance(i["@type"], list):
                    typ = i["@type"][0].split(":")
                    if typ[1] == "Class":
                        get_class(i["@id"], "Class")
                        try:
                            get_class(i["rdfs:subClassOf"]["@id"], "SuperClass")
                            super_class = i["rdfs:subClassOf"]["@id"]
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                        except KeyError:
                            pass
                    else:
                        get_property(i["@id"])
                else:
                    typ = i["@type"].split(":")
                    if typ[1] == "Class":
                        get_class(i["@id"], "Class")
                        try:
                            get_class(i["rdfs:subClassOf"]["@id"], "SuperClass")
                            super_class = i["rdfs:subClassOf"]["@id"]
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                        except KeyError:
                            pass
                    else:
                        get_property(i["@id"])
        else:
            print("@graph missing in " + filename)
    
    
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
            obj = json.load(obj_file)
            print(filename.replace("../../base-schemas/classes_expanded", ""), file=text_file)
            graph(obj)
