# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:01:22 2020

@author: SA20149963
"""

import csv
import os
import json

list_data = []

filename = "Wells.csv"
path = "D:\OSDU\Graph\data"
rec = 0
csv_columns = ['id','label','name','value','header','parent','relationship']
headers_tobe_ignored = ["Manifest","ExtensionProperties","properties", "GroupTypeProperties","IndividualTypeProperties","allOf", "Data"]
def get_json_instancefiles(path):
    paths =["D:\OSDU\Manifest_files\instances\well",
            "D:\OSDU\Manifest_files\instances\wellbore",
            "D:\OSDU\Manifest_files\instances\welllog"]
    for path in paths:
        for filename in os.listdir(path):
            if filename.endswith(".json"): 
                load_json_instance_file(filename, path)
                continue
            else:
                continue
   
def load_json_instance_file(filename, path):
    filepath = os.path.join(path,filename)
    json_file = open(filepath)
    json_data = json.load(json_file)
    json_file.close()
    list_data.clear()
    triples_creation_orchestrator(json_data)
    file_name= os.path.splitext(filename)[0]
    csv_path = "D:\OSDU\Graph\data"
    csv_path = os.path.join(csv_path,os.path.basename(path))
    generate_csv_file(file_name + ".csv", csv_path, csv_columns, list_data)

def create_element(key, value, parentid):
    dict_data = {}
    if key not in headers_tobe_ignored:
        node_id = autoIncrement()
        dict_data["id"] = node_id
        dict_data["label"] = key
        dict_data["name"] = key
        dict_data["value"] = value
        dict_data["header"] =key
        dict_data["parent"] =parentid
        dict_data["relationship"] = "has_" + key
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
        return node_id
    else:
        return parentid
def triples_creation_orchestrator(json_data):
    if "Manifest" in json_data.keys():
        
        parent_id = create_element("ResourceTypeID", json_data.get("ResourceTypeID"), 0)
        parent_id = create_element("ResourceID", json_data.get("Manifest")["ResourceID"], parent_id)
        parse_dictionary_collection(json_data, parent_id)
    elif "WorkProduct" in json_data.keys():
        
        parent_id = create_element("ResourceTypeID", json_data.get("WorkProduct")["ResourceTypeID"], 0)
        parse_dictionary_collection(json_data, parent_id)
   
def parse_dictionary_collection(json_data, parent_id):
    items_tobe_skipped = ["ResourceTypeID","ResourceID"]
    for key, value in json_data.items():
        if key not in items_tobe_skipped:
            if isinstance(value, dict):
                manage_sub_headers(key, value, parent_id)
            elif isinstance(value, list):
               
                manage_list_headers(key, value, parent_id)
            else:
                
                new_parent_id = create_element(key, value, parent_id)

def manage_list_headers(key, value, parent_id):
    print("list header.......%", key)
    new_parent_id = create_element(key, key, parent_id)
    parse_list_collection(key, value, new_parent_id)

def manage_sub_headers(key, value, parent_id):
    print("Dict header.......%", key)
    new_parent_id = create_element(key, key, parent_id)
    parse_dictionary_collection(value, new_parent_id)
    
def parse_list_collection(key, lst, parent_id):
    new_parent_id = ""
    for item in lst:
        if isinstance(item, dict):
            
            if "Mnemonic" in item.keys():
                manage_sub_headers("Mnemonic", item, parent_id)
            else:
                parse_dictionary_collection(item, parent_id)
        elif isinstance(item, list):
             
             manage_list_headers(key, item, parent_id)
             
        else:
             
             new_parent_id = create_element(key, item, parent_id)
    return new_parent_id



def generate_csv_file(filename, path, csv_columns, list_data):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        csv_file = os.path.join(path,filename)
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in list_data:
                writer.writerow(data)
    except IOError as e:
        print(str(e))

def autoIncrement():
 global rec
 pStart = 1 #adjust start value, if req'd 
 pInterval = 1 #adjust interval value, if req'd
 if (rec == 0): 
  rec = pStart 
 else: 
  rec = rec + pInterval 
 return str(rec).zfill(3)

get_json_instancefiles("")