# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:41:48 2020

@author: SA20149963
"""
from py2neo import Graph

from gremlin_python import statics
#from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from SPARQLWrapper import SPARQLWrapper, JSON, XML
import pandas as pd
import urllib.request
proxy = urllib.request.ProxyHandler({'http': 'ontology.osdu.com'}) 
opener = urllib.request.build_opener(proxy) 
urllib.request.install_opener(opener)
host = "40.117.46.5"
#driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))
#graph = Graph(host=host, user="neo4j",password= "admin", secure=False, port = 7687)
#graph = Graph()
#connection = DriverRemoteConnection('neo4j://40.117.46.5:7687', 'g')

#res = graph.run("match (n:Resource) return n")

sparql = SPARQLWrapper("https://raw.githubusercontent.com/GeoAssistant/GeoOntology/master/GeoAssisstant%20Ontology%20Step1and%202%20merged.owl", agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

res = sparql.setQuery('''SELECT *
                      WHERE {  ?s ?p ?o . }''')
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)
#results_df = pd.io.json.json_normalize(results['results']['bindings'])
#results_df[['item.value', 'itemLabel.value']]
#print (results_df  )
