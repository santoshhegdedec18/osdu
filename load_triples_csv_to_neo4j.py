# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:46:28 2020

@author: SA20149963
"""
from neo4j import GraphDatabase
import os
import re
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))

def get_json_instancefiles(path):
    paths =["D:\OSDU\Graph\instance_data\well",
            "D:\OSDU\Graph\instance_data\wellbore",
            "D:\OSDU\Graph\instance_data\welllog"]
    for path in paths:
        for filename in os.listdir(path):
            if filename.endswith(".json"): 
                load_json_instance_file(filename, path)
                continue
            else:
                continue
   




def create_element(tx, query):
    result = tx.run(query)
    for record in result:
       print(record)
       
def graph_creator(query):
      with driver.session() as session:
        session.write_transaction(create_element,query)