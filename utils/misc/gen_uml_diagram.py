#!/usr/local/bin/python3
import json
import os
import glob
import copy
import subprocess


folder_path = "../../generated/"
if not os.path.exists("../../diagrams/"):
    os.makedirs("../../diagrams/")
diagram_path = "../../diagrams/"
dup_classes = []
with open(diagram_path + "IUDX-Vocab-Ontology.txt", "w+") as text_file:
    print("@startuml", file=text_file)
    print("title IUDX-VOC Ontology Diagram" + "\n", file=text_file)
    print("left to right direction" + "\n" + "skinparam classFontColor DarkCyan" + "\n" + "skinparam roundcorner 27" + "\n", file=text_file)
    

    def graph(obj):
        if "@graph" in obj.keys():
            graph_obj = copy.deepcopy(obj["@graph"])
            for i in obj["@graph"]:
                if isinstance(i["@type"], list):
                    typ = i["@type"][0].split(":")
                    if typ[1] == "Class":
                        class_name = i["@id"]
                        cname = i["@id"].split(":")
                        cname = "".join(cname)
                        if class_name not in dup_classes:
                            dup_classes.append(class_name)
                            print("class " + "\"" + class_name + "\"" + " as " + cname + "{", file=text_file) 
                            for j in graph_obj:
                                for prop in j["@type"]:
                                    if "Property" in prop:
                                        print("\t" + j["@id"], file=text_file)
                                    elif "Relationship" in prop:
                                        print("\t" + j["@id"], file=text_file)
                            print("}", file=text_file)
                            try:
                                if "rdf:" in i["rdfs:subClassOf"]["@id"]:
                                    spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                                    superclass_name = "".join(spclass_name)
                                    super_class = i["rdfs:subClassOf"]["@id"]
                                    print("class " + "\"" + i["rdfs:subClassOf"]["@id"] + "\" "+ "as " + superclass_name, file=text_file)
                                    if "rdf:" not in super_class:
                                        super_class = super_class.split(":")
                                        with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                            super_obj = json.load(super_file)
                                            graph(super_obj)
                                    print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                                elif "rdf:" not in i["rdfs:subClassOf"]["@id"]:
                                    spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                                    superclass_name = "".join(spclass_name)
                                    super_class = i["rdfs:subClassOf"]["@id"]
                                    if "rdf:" not in super_class:
                                        super_class = super_class.split(":")
                                        with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                            super_obj = json.load(super_file)
                                            graph(super_obj)
                                    print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                            except KeyError:
                                pass
                elif "Class" in i["@type"]:
                    typ = i["@type"].split(":")
                    if typ[1] == "Class":
                        class_name = i["@id"]
                        cname = i["@id"].split(":")
                        cname = "".join(cname)
                        if class_name not in dup_classes:
                            dup_classes.append(class_name)
                            print("class " + "\"" + class_name + "\"" + " as " + cname + "{", file=text_file) 
                            for j in graph_obj:
                                for prop in j["@type"]:
                                    if "Property" in prop:
                                        print("\t" + j["@id"], file=text_file)
                                    elif "Relationship" in prop:
                                        print("\t" + j["@id"], file=text_file)
                            print("}", file=text_file)
                            try:
                                if "rdf:" in i["rdfs:subClassOf"]["@id"]:
                                    spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                                    superclass_name = "".join(spclass_name)
                                    super_class = i["rdfs:subClassOf"]["@id"]
                                    print("class " + "\"" + i["rdfs:subClassOf"]["@id"] + "\" "+ "as " + superclass_name, file=text_file)
                                    if "rdf:" not in super_class:
                                        super_class = super_class.split(":")
                                        with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                            super_obj = json.load(super_file)
                                            graph(super_obj)
                                    print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                                elif "rdf:" not in i["rdfs:subClassOf"]["@id"]:
                                    spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                                    superclass_name = "".join(spclass_name)
                                    super_class = i["rdfs:subClassOf"]["@id"]
                                    if "rdf:" not in super_class:
                                        super_class = super_class.split(":")
                                        with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                            super_obj = json.load(super_file)
                                            graph(super_obj)
                                    print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                            except KeyError:
                                pass
        else:
            print("@graph missing in " + filename)
    #filename = "../../generated/Resource.jsonld"
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
             obj = json.load(obj_file)
             graph(obj)
    print("\n" + "@enduml", file=text_file)
which_plantuml = ((subprocess.check_output("which plantuml", shell=True)).decode("utf-8")).rstrip()
subprocess.call([which_plantuml, diagram_path + "IUDX-Vocab-Ontology.txt"])
