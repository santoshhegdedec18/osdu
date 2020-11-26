# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 19:33:10 2020

@author: SA20149963
"""

import json
import types

from owlready2 import * 
from owlready import *  
uri = r"http://ontology.osdu.com/osdu_ontology.owl"
#Load Ontology .owl file through file URI, the method can also create a new file if not exists already
osdu_onto = get_ontology(uri)
headers_tobe_ignored = ["Manifest","ExtensionProperties","properties", "GroupTypeProperties","IndividualTypeProperties","allOf", "Data"]

def get_json_instancefiles_for_well():
    path = "D:\OSDU\Manifest_files\instances\well"
    for filename in os.listdir(path):
        if filename.endswith(".json"): 
            load_json_instance_file(filename, path, osdu_onto.WELL)
            continue
        else:
            continue
   
def load_json_instance_file(filename, path, ontoclass):
    filepath = os.path.join(path,filename)
    json_file = open(filepath)
    json_data = json.load(json_file)
    json_file.close()
    file_name= os.path.splitext(filename)[0]
    triples_creation_orchestrator(json_data, file_name, ontoclass)
     
def triples_creation_orchestrator(json_data, individual_name, ontoclass):
    propname = "has_well"
    class propname(DataProperty):
          ontology = osdu_onto
          range = [str]
    my_individual = ontoclass(individual_name)
    my_individual.has_well = "yes"
    print(my_individual.has_well)
    #parse_dictionary_collection(json_data, parent_id)
   

get_json_instancefiles_for_well()