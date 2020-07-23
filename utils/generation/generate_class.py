#!/usr/local/bin/python3
import json
import os
from os import walk
import glob
import shutil

from collections import OrderedDict
from distutils.dir_util import copy_tree


data_models_dir = "data-models"

excluded = ["utils", "examples", "generated", "diagrams", ".git"]

examples_dir = "examples"


# Recursively list out classes and properties paths

from_classes = []
from_properties= []
from_examples = []

for (dirpath, dirnames, filenames) in os.walk("./"):

    if (len([dirpath.find(e) for e in excluded if dirpath.find(e)>0])):
        if(dirpath.find(examples_dir)>0):
            from_examples.append(dirpath)
        continue

    if(dirpath.find("classes")>0 and dirpath.find("properties")==-1 ):
        from_classes.append(dirpath)

    if(dirpath.find("properties")>0):
        from_properties.append(dirpath)


classes_path = "/tmp/all_classes/"
properties_path = "/tmp/all_properties/"
examples_path = "/tmp/all_examples"
tmp_expanded_path = "/tmp/generated/"



if not os.path.exists("generated/"):
    os.makedirs("generated/")
if not os.path.exists(examples_path):
    os.makedirs(examples_path)

generated_path = "/tmp/generated_classes/"



def gen_examples():
    for fldr in from_examples:
        copy_tree(fldr, examples_path)




def find(element, array):
    for item in array:
        if item['@id'] == element:
            return item

def generate(class_path, property_path):
    for class_file in glob.glob(os.path.join(class_path, '*.jsonld')):
        domain = class_file.replace(class_path, "")
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
            for prop_file in glob.glob(os.path.join(property_path, '*.jsonld')):
                with open(prop_file, "r+") as prop_obj:
                    prop = json.load(prop_obj)
                    if "@graph" in prop.keys():
                        try:
                            includes = find(domain, prop["@graph"][0]["iudx:domainIncludes"])
                            if includes is not None:
                                new_dict["@graph"].append(prop["@graph"][0])
                        except KeyError:
                            pass
                            #print("iudx:domainIncludes not in " + prop_file)
                        # try:
                        #     includes = find(domain, prop["@graph"][0]["iudx:rangeIncludes"])
                        #     if includes is not None:
                        #         print(includes)
                        #         print(prop["@graph"][0])
                        #         new_dict["@graph"].append(prop["@graph"][0])
                        # except KeyError:
                        #     pass
                        #     #print("iudx:rangeIncludes not in " + prop_file)
                    else:
                        print("@graph missing in " + prop_file)
            os.makedirs(os.path.dirname(tmp_expanded_path), exist_ok=True)
            with open(tmp_expanded_path + 
                    domain.replace("iudx:", "") + ".jsonld", "w+") as new_file:
                json.dump(new_dict, new_file, indent=4)


def super_class(prop, expanded_dict):
    try:
        if "rdf:" not in prop["rdfs:subClassOf"]["@id"]:
            with open(tmp_expanded_path + 
                    prop["rdfs:subClassOf"]["@id"].split(":")[1] + ".jsonld", "r") as super_file:
                super_obj = json.load(super_file)
                for sub_prop in super_obj["@graph"]:
                    expanded_dict["@graph"].append(sub_prop)
                    super_class(sub_prop, expanded_dict)
    except KeyError:
        pass


def generate_expanded():
    for expanded_file in glob.glob(os.path.join(tmp_expanded_path, '*.jsonld')):
        with open(expanded_file, "r+") as super_obj_file:
            expanded_dict = OrderedDict()
            obj = json.load(super_obj_file)
            if "@context" in obj.keys():
                expanded_dict["@context"] = obj["@context"]
                del(obj["@context"]) 
            else:
                print("@context missing in " + expanded_file)
            if "@graph" in obj.keys():
                expanded_dict["@graph"] = obj["@graph"]
                try:
                    sub_class = obj["@graph"][0]["rdfs:subClassOf"]["@id"]
                    if "rdf:" not in sub_class:
                        with open(tmp_expanded_path +
                                sub_class.split(":")[1] + ".jsonld", "r") as parent_file:
                            parent_obj = json.load(parent_file)
                            for sub_prop in parent_obj["@graph"]:
                                expanded_dict["@graph"].append(sub_prop)
                                super_class(sub_prop, expanded_dict)
                except KeyError:
                    pass
            os.makedirs(os.path.dirname(generated_path), exist_ok=True)
            with open(generated_path + 
                    expanded_file.replace(tmp_expanded_path, ""), "w+") as new_file:
                json.dump(expanded_dict, new_file, indent=4)


if __name__=="__main__":
    for directory in from_classes:
        copy_tree(directory, classes_path)
    for directory in from_properties:
        copy_tree(directory, properties_path)
    generate(classes_path, properties_path)
    generate_expanded()
    gen_examples()
