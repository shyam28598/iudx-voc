import json
import sys
import os

"""Create expanded class form of iudx classes by introspecting properties
"""

properties_dir = "properties/"
classes_dir = "classes/"
classes_generated_dir = "classes_expanded/"


properties = {}

for fl in os.listdir(properties_dir):
    with open(os.path.join(properties_dir, fl), "r") as f:
        try:
            properties[fl[:-7]] = json.load(f)
        except Exception as e:
            print("Property - " + fl[:-7] + " not valid json")
            print(e)

classes = {}
for p in properties.keys():
    try:
        cls = properties[p]["iudx:domainIncludes"]
        if type(cls) is dict:
            cl_names = [cls["@id"]]
        elif type(cls) is list:
            cl_names = [c["@id"] for c in cls]
    except Exception as e:
        print("Property - " + p + " has no class")
        print(e)
        continue

    for c in cl_names:
        if c not in classes.keys():
            classes[c] = [properties[p]]
        else:
            try:
                classes[c].append(properties[p])
            except Exception as e:
                print(properties[p])
                print(e)


for fl in os.listdir(classes_dir):
    with open(os.path.join(classes_dir, fl), "r") as f:
        cls = json.load(f)
    if fl[:-7] not in classes.keys():
        print("Class - " + fl[:-7] + " doesn't exist")
        continue
    for props in classes[fl[:-7]]:
        cls["@context"] = list(set(props["@context"]) + cls["@context"])
    print(cls)
