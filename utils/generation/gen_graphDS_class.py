#!/usr/local/bin/python3
import json
import copy
import os
import glob

all_paths = ["../../base-schemas/classes/",
            "../../base-schemas/properties/",
            "../../data-models/classes/",
            "../../data-models/properties/"]

fundamental_types = ["iudx:QuantitativeProperty", "iudx:TimeProperty",
                    "iudx:TextProperty", "iudx:GeoProperty",
                    "iudx:StructuredProperty", "iudx:Relationship"]

new_list = []
new_dict = {"@graph": []}
graph = {}
expanded = {"@context": {}, "@graph": []}
graph_lookup = {}
#path = "/tmp/"
#graph_file = "iudx-ld.jsonld"


if not os.path.exists("../../expanded/"):
    os.makedirs("../../expanded/")
expanded_path = "../../expanded/"


def gen_graph(folder_path):
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
            obj = json.load(obj_file)
            if "@context" in obj.keys():
                del(obj["@context"]) 
            else:
                print("@context missing in " + filename)
            if "@graph" in obj.keys():
                new_list = obj["@graph"]
                new_dict["@graph"].append(new_list[0])
            else:
                print("@graph missing in " + filename)
    with open("/tmp/iudx-ld.jsonld", "w+") as ld_file:
        json.dump(new_dict, ld_file, indent=4)

def gen_expanded():
    with open("/tmp/iudx-ld.jsonld", "r") as f:
        graph = json.load(f)["@graph"]
   
    for item in graph:
        if "rdfs:Class" in item["@type"]:
            cls_name = item["@id"]
            tmp_cls = copy.deepcopy(expanded)
            tmp_cls["@graph"].append(copy.deepcopy(item))
            for prop in graph:
                if prop["@type"][0] in fundamental_types:
                    # Get domains
                    for rng in prop["iudx:domainIncludes"]:
                        if rng["@id"] == cls_name:
                            tmp_cls["@graph"].append(copy.deepcopy(prop))
                    # Get ranges
                    for rng in prop["iudx:rangeIncludes"]:
                        if rng["@id"] == cls_name:
                            tmp_cls["@graph"].append(copy.deepcopy(prop))
    
    
                graph_lookup[cls_name] = copy.deepcopy(tmp_cls)
                with open("../../expanded/"+cls_name.split(":")[1]+".jsonld", "w+") as f:
                    json.dump(tmp_cls, f, indent=4)
    
    #with open("./graph_lookup.jsonld", "w+") as gf:
    #    json.dump(graph_lookup, gf, indent=4)


if __name__ == "__main__":
    for path in all_paths:
        gen_graph(path)
        gen_expanded()
