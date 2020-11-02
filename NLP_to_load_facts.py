# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:46:28 2020

@author: SA20149963
"""
from neo4j import GraphDatabase
import os
import re
import json
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))

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
    
    file_name= os.path.splitext(filename)[0]
    html_path = "D:\OSDU\Graph\data"
    html_path = os.path.join(html_path,os.path.basename(path))
    load_json_data_to_NLP(json_data, "load_log_1013_akm11_1978_comp_las.json")
    #generate_csv_file(file_name + ".csv", csv_path, csv_columns, list_data)
def load_json_data_to_NLP(json_data,file ):
    fileurl = "/import/jsonmetadata/" + file
    query = '''WITH "/import/jsonmetadata/'''+file+'''" AS url 
    CALL apoc.load.json(url) YIELD value  WITH value MERGE(a:Article{uri: "'''+fileurl+'''", body:"'''+str(json_data)+'''" }) return a'''
    
    graph_creator(query)
    get_entities_from_NLP(fileurl)
def get_entities_from_NLP(uri):
    
 
    
    query = ''' 
    MATCH (a:Article{uri: "'''+uri+'''"})
    CALL apoc.nlp.azure.entities.stream(a,{
    key:"9f5b2b36a83c4022ae27fa5ada424468", 
    url:"https://osdu-cognitive-service.cognitiveservices.azure.com/", 
    nodeProperty: 'body'} ) yield value 
    UNWIND value.entities AS entity RETURN entity'''
    print (query)
    graph_creator(query)

def create_element(tx, query):
    result = tx.run(query)
    for record in result:
       print(record)
       
def graph_creator(query):
      with driver.session() as session:
        session.write_transaction(create_element,query)

get_json_instancefiles("")