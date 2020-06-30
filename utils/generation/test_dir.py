import os

path = "data-models"


f = []

class_folders = []
properties_folders = []



def getPaths(path):
    for (dirpath, dirnames, filenames) in os.walk(path):

        if(dirpath.find("classes")>0 and 
                dirpath.find("properties")==-1 and dirpath.find("examples")==-1):
            class_folders.append(dirpath)

        if(dirpath.find("properties")>0 and dirpath.find("examples")==-1):
            print(dirpath)
            properties_folders.append(dirpath)

getPaths(path)
print(class_folders)
print(properties_folders)
