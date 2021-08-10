import os
import json
from collections import OrderedDict
import shutil



classes = ['owl:Class', 'rdfs:Class']
properties = ["iudx:TextProperty", "iudx:QuantitativeProperty", "iudx:StructuredProperty", "iudx:GeoProperty", "iudx:TimeProperty", "iudx:Relationship", 'rdf:Property'] 
relation = ["iudx:Relationship"]
class_folder_path = "/tmp/all_classes/"
properties_folder_path = "/tmp/all_properties/"
examples_path = "/tmp/all_examples"


relation_list = ["domainOf", "subClassOf", "rangeOf"]
error_list = []


                    

class Vertex:
    def __init__(self, node, vertice_type, jsonld, context) -> None:
        self.id = node
        self.node_type = vertice_type
        self.adjacent = {}
        self.jsonld = jsonld
        self.context = context

    def __str__(self) -> str:
        print(str(self.id))

    def add_neighbour(self, neighbour, relationship):
        self.adjacent[neighbour] = relationship
    
    def get_connections(self):
        return(self.adjacent.keys())

    def get_weight(self, neighbour):
        return(self.adjacent[neighbour])

    def get_id(self):
        return(self.id)

    def get_type(self):
        return(self.node_type)


            

class Graph:
    def __init__(self) -> None:
        self.vertices = {}
        self.num_of_vertices = 0
        
    def __iter__(self) -> None:
        return(iter(self.vertices.values()))

    def add_vertex(self, node, tp, jsonld, context):
        self.num_of_vertices = self.num_of_vertices + 1
        new_vertex = Vertex(node, tp, jsonld, context)
        self.vertices[node] = new_vertex
        return new_vertex

    def add_edge(self,vertex_from, vertex_to, relationship): 
        self.vertices[vertex_from].add_neighbour(self.vertices[vertex_to], relationship)
        
    def get_children(self, v, out = {"@graph":[],"@context":{}}):
        for key, value in v.adjacent.items():
            if value == "domainOf":
                out["@graph"].append(key.jsonld)
                out["@context"].update(key.context)
            elif value == "subClassOf":
                out["@graph"].append(key.jsonld)
                out["@context"].update(key.context)
                self.get_children(key, out)
            elif value == "rangeOf":
                out["@graph"].append(key.jsonld)
                out["@context"].update(key.context)
                self.get_children(key, out)
    
    def get_class_graph (self, v, out = {"@graph":[],"@context":{}}):
        out["@graph"].append(v.jsonld)
        out["@context"].update(v.context)
        self.get_children(v,out)

    def get_vertex(self, search):
        if search in self.vertices:
            return(self.vertices[search])
        else:
            return None
    
    def get_all_vertices(self):
        return(self.vertices.keys())



class Vocabulary:
    
    def __init__(self, path_to_json):
        self.json_ld_graph = []
        self.visited = {}
        self.read_repo(path_to_json)
        self.g = Graph()
        self.build_graph()

    def read_repo(self, path_to_json):
        for subdir, dirs, files in os.walk(path_to_json):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".jsonld"):
                    with open(filepath,"r+") as input_file:
                        data = json.load(input_file)
                        if "@graph" in data:
                            self.json_ld_graph.append({"@graph":data["@graph"][0],"@context":data["@context"]})
                        


    def build_graph(self):
        for n in self.json_ld_graph:
            try:
                # Making vertices of all classes  
                if (any(ele in classes for ele in n["@graph"]["@type"])):
                    tp = "Class"
                    self.g.add_vertex(n["@graph"]["@id"], tp, n["@graph"], n["@context"])
                    self.visited[n["@graph"]["@id"]] = False
                # Making vertices of all properties
                if (any(ele in properties for ele in n["@graph"]["@type"])):
                    tp = "Property"
                    self.g.add_vertex(n["@graph"]["@id"], tp, n["@graph"], n["@context"])
                    self.visited[n["@graph"]["@id"]] = False
            except:
                pass 
                

        for n in self.json_ld_graph:
                if "rdfs:subClassOf" in n["@graph"]:
                    try:
                        self.g.add_edge(n["@graph"]["@id"], n["@graph"]["rdfs:subClassOf"]["@id"], "subClassOf")
                    except Exception as error:
                        error_list.append({"type ": "subClassOf missing" , "in": n["@graph"]["@id"]})
                        pass
                        
                if "iudx:domainIncludes" in n["@graph"] :
                    for i in n["@graph"]["iudx:domainIncludes"]:
                        try:
                            self.g.add_edge(n["@graph"]["@id"], i["@id"], "domainIncludes")
                            self.g.add_edge(i["@id"], n["@graph"]["@id"], "domainOf")      
                        except Exception as error:
                            error_list.append({"type ": "domainIncludes missing" , "value": i["@id"], "in": n["@graph"]["@id"]})
                            pass
                        
                if "iudx:rangeIncludes" in n["@graph"] :
                    for i in n["@graph"]["iudx:rangeIncludes"]:
                        try:
                            self.g.add_edge(n["@graph"]["@id"], i["@id"], "rangeIncludes")
                            self.g.add_edge(i["@id"], n["@graph"]["@id"], "rangeOf")
                        except Exception as error:
                            error_list.append({"type" : "rangeIncludes missing", "value" : i["@id"], "in": n["@graph"]["@id"]})
                            pass
    
    def make_classfile(self):
        for n in self.g:
            if n.node_type == "Class":
                k = self.g.get_vertex(n.id)
                grph = {"@graph":[],"@context":{}}
                self.g.get_class_graph(k, grph)
                name_list = k.id.split(":")
                with open(class_folder_path + name_list[1] + ".jsonld", "w") as context_file:
                    json.dump(grph,context_file, indent=4)


    def is_loop(self, v, visited={}, root=str):
        visited[v.id] = True
        for key, value in v.adjacent.items():
            if value in relation_list:
                if visited[key.id] == False:
                    if(self.is_loop(key, visited, v.id)):
                        return True
                elif root!=key.id:
                    return True
        return False

    def make_master(self):
            master_dict = OrderedDict()
            master_dict = {"@context":{}}
            with open("iudx.jsonld" , "w") as master_file:
                for n in self.json_ld_graph:
                    master_dict["@context"][str(n["@graph"]["@id"].split(":")[-1])] = {"@id":n["@graph"]["@id"]}
                    if "iudx:Relationship" in n["@graph"]["@type"]:
                         master_dict["@context"][str(n["@graph"]["@id"].split(":")[-1])] = {"@id":n["@graph"]["@id"], "@type":"@id"}
                    master_dict["@context"]["type"] = "@type"
                    master_dict["@context"]["id"] = "@id"
                    master_dict["@context"]["@vocab"] =  "https://voc.iudx.org.in/"
                    master_dict["@context"]["rdfs"] =  "http://www.w3.org/2000/01/rdf-schema#"
                    master_dict["@context"]["skos"] = "http://www.w3.org/2004/02/skos/core#"
                    master_dict["@context"]["schema"]= "http://schema.org/"
                    master_dict["@context"]["owl"]= "http://www.w3.org/2002/07/owl#"
                    master_dict["@context"]["iudx"] = "https://voc.iudx.org.in/"
                    master_dict["@context"]["geojson"] = "https://purl.org/geojson/vocab#"
                    master_dict["@context"]["rdf"] =  "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                    master_dict["@context"]["xsd"] = "http://www.w3.org/2001/XMLSchema#"
                    master_dict["@context"]["qudt"] =  "http://qudt.org/vocab/unit/"
                json.dump(master_dict, master_file, indent = 4)


    def gen_examples(self):
        try:
            shutil.copytree("./examples/", examples_path)
        except Exception as e:
            pass



    def make_propertiesfile(self):
        for n in self.g:
            if n.node_type == "Property":
                grph = {"@graph":[],"@context":{}}
                grph["@graph"].append(n.jsonld)
                grph["@context"].update(n.context)  
                name_list = n.id.split(":")
                with open(properties_folder_path + name_list[1] + ".jsonld", "w") as context_file:
                    json.dump(grph,context_file, indent=4)
        
        with open("errors.json", "w") as out_file:
            json.dump(error_list, out_file)


def main():


    if not os.path.exists(class_folder_path):
        os.makedirs(class_folder_path)

    if not os.path.exists(properties_folder_path):
        os.makedirs(properties_folder_path)

    voc = Vocabulary("./")
    voc.make_classfile()
    voc.make_propertiesfile()
    voc.make_master()
    voc.gen_examples()
    

if __name__ == "__main__":
    main()
