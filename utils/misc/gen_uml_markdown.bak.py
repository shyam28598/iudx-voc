#!/usr/local/bin/python3
import json
import os
import glob
import copy


folder_path = "../../generated/"

with open("./plantuml_markdown.txt", "w+") as text_file:
    print("@startuml", file=text_file)
    print("title IUDX-VOC Ontology Diagram" + "\n", file=text_file)
    

    def graph(obj):
        if "@graph" in obj.keys():
            graph_obj = copy.deepcopy(obj["@graph"])
            for i in obj["@graph"]:
                if isinstance(i["@type"], list):
                    typ = i["@type"][0].split(":")
                    if typ[1] == "Class":
                        #if "iudx:" in i["@id"]:
                        print(i["@id"])
                        class_name = i["@id"].split(":")
                        print("class \"" + i["@id"] + "\" as " + class_name[1] + "{", file=text_file) 
                        for j in graph_obj:
                            for prop in j["@type"]:
                                if "Property" in prop:
                                    print("\t" + j["@id"], file=text_file)
                                elif "Relationship" in prop:
                                    print("\t" + j["@id"], file=text_file)
                        print("}", file=text_file)
                        #else:
                        #    print("class \"" + i["@id"] + "\" as " + i["@id"].replace(":","") + "{", file=text_file) 
                        #    for j in graph_obj:
                        #        for prop in j["@type"]:
                        #            if "Property" in prop:
                        #                print("\t" + j["@id"], file=text_file)
                        #            elif "Relationship" in prop:
                        #                print("\t" + j["@id"], file=text_file)
                        #    print("}", file=text_file)
                        try:
                            superclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                            super_class = i["rdfs:subClassOf"]["@id"]
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                            print(superclass_name[1] + " --|> " + class_name[1] + " : SubClass", file=text_file)
                        except KeyError:
                            pass
                elif "Class" in i["@type"]:
                    typ = i["@type"].split(":")
                    if typ[1] == "Class":
                        #if "iudx:" in i["@id"]:
                        print(i["@id"])
                        class_name = i["@id"].split(":")
                        print("class \"" + i["@id"] + "\" as " + class_name[1] + "{", file=text_file) 
                        for j in graph_obj:
                            for prop in j["@type"]:
                                if "Property" in prop:
                                    print("\t" + j["@id"], file=text_file)
                                elif "Relationship" in prop:
                                    print("\t" + j["@id"], file=text_file)
                        print("}", file=text_file)
                        #else:
                        #    print("class \"" + i["@id"] + "\" as " + i["@id"].replace(":","") + "{", file=text_file) 
                        #    for j in graph_obj:
                        #        for prop in j["@type"]:
                        #            if "Property" in prop:
                        #                print("\t" + j["@id"], file=text_file)
                        #            elif "Relationship" in prop:
                        #                print("\t" + j["@id"], file=text_file)
                        #    print("}", file=text_file)
                        try:
                            superclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                            super_class = i["rdfs:subClassOf"]["@id"]
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                            print(superclass_name[1] + " --|> " + class_name[1] + " : SubClass", file=text_file)
                        except KeyError:
                            pass
        else:
            print("@graph missing in " + filename)
    

    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
             obj = json.load(obj_file)
             #print(filename.replace("../../base-schemas/classes_expanded", ""))
             graph(obj)
    print("\n" + "@enduml", file=text_file)
