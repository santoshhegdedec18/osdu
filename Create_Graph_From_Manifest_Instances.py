# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 17:57:15 2020

@author: SA20149963
"""
from neo4j import GraphDatabase
import json
import os
import re
import sys
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))
props_tobe_ignored = ["type", "pattern", "format", "$ref"]
headers_tobe_ignored = ["Manifest","ExtensionProperties","properties", "GroupTypeProperties","IndividualTypeProperties","allOf", "Data"]
root_element_collection = {"srn:type:master-data/Well:":"WELL", "srn:type:master-data/Wellbore:":"WELLBORE",
                           "srn:type:work-product/WellLog:":"WELLLOG", "srn:type:work-product-component/WellLog:":"WELLLOG",
                           "srn:type:file/las2:":"WELLLOG"}
all_resource_types = ["srn:type:master-data/Well:", "srn:type:master-data/Wellbore:", 
                  "srn:type:work-product/WellLog:", "srn:type:work-product-component/WellLog:", 
                  "srn:type:file/las2:"]
well_wellbore_types = ["srn:type:master-data/Well:", "srn:type:master-data/Wellbore:"]

def get_root_element_name(value):
    return str(root_element_collection[value])

def initiate_graph_creation():
    paths =["D:\OSDU\Manifest_files\instances\well",
            "D:\OSDU\Manifest_files\instances\wellbore",
            "D:\OSDU\Manifest_files\instances\welllog"]
    for path in paths:
        for filename in os.listdir(path):
            if filename.endswith(".json"): 
                load_manifest_instance_json(filename, path)
                continue
            else:
                continue    
def load_manifest_instance_json(filename, path):
    fullpath = os.path.join(path, filename)
    #print ("file details %, %", fullpath)
    file = open(fullpath)
    json_data = json.load(file)
    file.close()
    graph_orchestrator(json_data,"" )
    driver.close() 

def graph_orchestrator(json_data, parentelement):
     #Delete all nodes and relationships before creating the elements
    if parentelement == "":
        delete_all_query = "match(n:wellogs) detach delete n"
        graph_creator(delete_all_query)
        root_element_query= '''MERGE(well:Well {name:"WELL", value:"Well"})
                               MERGE(wellbore:Wellbore{name:"WELLBORE", value:"Wellbore"})
                               MERGE(welllog:Welllog{name:"WELLLOG", value:"Welllog"})
                               WITH well, wellbore, welllog 
                               MERGE(well)-[:has_Wellbore]->(wellbore)
                               MERGE (wellbore)-[:has_Welllog]->(welllog)'''
        graph_creator(root_element_query)
    #sys.exit()
    if isinstance(json_data, dict):
        handle_dictionary_object(json_data, parentelement)
    elif isinstance(json_data, list):
        handle_list_object(json_data, parentelement)
    else:
        print("Single element with key, value..... %",json_data, type(json_data))

# Method is called to handle a sub dictionary object from a parent dictionary recursively
def handle_dictionary_object(dic, pelement):
      parentelement = pelement
      resourcetype = ""
      for key, value in dic.items():
            if key == "ResourceTypeID":
                resourcetype = value
            if resourcetype in well_wellbore_types:
                if key=="ResourceID" and pelement=="":
                    parentelement = key
                    
                    nodequery = '''MERGE ( '''+key +''':Welllog {name:"'''+key+'''", value:"'''+value+'''"})
                    WITH '''+key+''' MATCH (a),(b) where a.name="'''+get_root_element_name(value)+'''" and b.value = "'''+value+'''" 
                    WITH a,b MERGE(b)<-[:has_'''+value.replace("-","_").replace(":","_").replace("/","_") +''']-(a)'''
                             
                    graph_creator(nodequery)
                    
                if not type(value) == bool and isinstance(value, dict):
                    pe = handle_group_headers(key, parentelement)
                    graph_orchestrator(value, pe)
                    
                elif not type(value) == bool and isinstance(value, list):
                    pe = handle_group_headers(key, parentelement)
                    handle_list_object(key, value, pe)
                    
                else:
                    handle_single_dictionary_element(key, value, parentelement)
            else:
                print("implement work products...%", value)

# Method is called to create graph elements and relationships recursively 
def handle_single_dictionary_element(key, value, parentelement):
    if not key == parentelement:
        nodequery = '''MERGE ( '''+str(key) +''':Welllog {name:"'''+str(key)+'''", value:"'''+str(value)+'''"})
        WITH '''+str(key)+''' MATCH (a),(b) where a.name="'''+parentelement+'''" and b.value = "'''+str(value)+'''" 
        WITH a,b MERGE(b)<-[:has_'''+str(key)+''']-(a)'''
        graph_creator(nodequery)
    
#Method is called to create classes from a list object recursively
def handle_list_object(key, lst, parentelement):
    for item in lst:
        if isinstance(item,list):
           
           print("This is a list object.... elements not created..%", item)
        else:
            graph_orchestrator(item,parentelement)
 
# Method called to create sub class for the group headers whenever required
def handle_group_headers(key, parentelement):
    pe = parentelement
    if key not in headers_tobe_ignored:
        nodequery = '''MERGE ( '''+str(key) +''':Welllog {name:"'''+str(key)+'''"})
        WITH '''+str(key)+''' MATCH (a),(b) where a.name="'''+parentelement+'''" and b.name = "'''+str(key)+'''" 
        WITH a,b MERGE(b)<-[:has_'''+str(key)+''']-(a)'''
        parentelement = str(key)
        graph_creator(nodequery)
    return parentelement
               
def create_element(tx, query):
    result = tx.run(query)
    for record in result:
       print(record)
       
def graph_creator(query):
      with driver.session() as session:
        session.write_transaction(create_element,query)
        

initiate_graph_creation()