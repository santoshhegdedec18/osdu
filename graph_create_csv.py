# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:36:40 2020

@author: SA20149963
"""

import csv
import os
import json

list_data = []
parent_id = {"parent":0, "top_node":0}
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
    parse_dictionary_collection(json_data, "")
    file_name= os.path.splitext(filename)[0]
    csv_path = "D:\OSDU\Graph\data"
    csv_path = os.path.join(csv_path,os.path.basename(path))
  
    generate_csv_file(file_name + ".csv", csv_path, csv_columns, list_data)

def get_parent_element(key, value, header):
    
    dict_data = {}
    if key == "ResourceTypeID" and header=="":
        node_id = autoIncrement()
        dict_data["id"] = node_id
        dict_data["label"] = key
        dict_data["name"] = key
        dict_data["value"] = value
        dict_data["header"] = ""
        dict_data["parent"] =header
        dict_data["relationship"] = "has_" + key
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
        parent = key
    elif key == "ResourceID":
        node_id = autoIncrement()
        dict_data["id"] = node_id
        dict_data["label"] = key
        dict_data["name"] = key
        dict_data["value"] = value
        dict_data["header"] = "ResourceTypeID"
        dict_data["parent"] =header
        dict_data["relationship"] = "has_" + key
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
        parent = key
    
    return header

def parse_dictionary_collection(input_collection,parent_ky):
    parent =parent_ky
    global prev_header
    
    for key, value in input_collection.items():
         if key == "ResourceTypeID" or key == "ResourceID":
             parent = get_parent_element(key, value, parent)
             parent_ky = parent             
         if isinstance(value, dict):
             
             parent = parse_group_header_element(key, value, parent_ky)
             parent = parse_dictionary_collection(value, key)
             
         elif isinstance(value, list):
             parent = parse_group_header_element(key, value, parent_ky)
             parent = parse_list_colleciton(value, key)
             
         else:
            
             parent = create_triples_for_single_dict_element(key, value, parent)
             
    return parent
    
def parse_list_colleciton(lst, pelement):
    parent = pelement
    for item in lst:
        if isinstance(item, list):
            parent = parse_group_header_element(item, "", parent)
            parent = parse_list_colleciton(item, parent, "")
        elif isinstance(item, dict):
            parent = parse_dictionary_collection(item, parent)
        else:
            parent = create_triples_for_single_list_element(item, parent)
    return parent

def parse_group_header_element(key, value, parent):
    dict_data = {}
    pe = parent
    if key not in headers_tobe_ignored:
        node_id = autoIncrement()
        dict_data["id"] = node_id
        dict_data["label"] = key
        dict_data["name"] = key
        dict_data["value"] = key
        dict_data["header"] = key
        dict_data["parent"] = pe
        dict_data["relationship"] = "has_" + key
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
        #parent_id.update({"parent":node_id})
        pe = key
    return pe 
          
def create_triples_for_single_dict_element(key, value, pelement):
    print("Triple for single dictionaly element....%", key)
    parent = pelement
    node_id = autoIncrement()
    dict_data = {}
    props_ignored = ["ResourceID", "ResourceTypeID"]
    if key not in props_ignored:
        dict_data["id"] =  node_id
        dict_data["label"] = key
        dict_data["name"] = key
        dict_data["value"] = value
        dict_data["header"] = parent
        dict_data["parent"] = parent
        dict_data["relationship"] ="has_" +key
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
    return parent    
   
    
    
def create_triples_for_single_list_element(value, pelement):
    print("Triple for single list element....%",value)
    parent = pelement
    node_id = autoIncrement()
    dict_data = {}
    props_ignored = ["ResourceID", "ResourceTypeID"]
    if value not in props_ignored:
        dict_data["id"] =  node_id
        dict_data["label"] = value
        dict_data["name"] = value
        dict_data["value"] = value
        dict_data["header"] = parent
        dict_data["parent"] = parent
        dict_data["relationship"] ="has" 
        dict_data_copy = dict_data.copy()
        list_data.append(dict_data_copy)
    return parent    
    
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
#print(list_data)
