# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:41:48 2020

@author: SA20149963
"""

from SPARQLWrapper import SPARQLWrapper, XML, N3, RDF, CSV, TSV, RDFXML, JSON
#import requests
#import json
try:
    url = "http://52.177.66.34:8080/fuseki/osdu_vocabulory"
   
   
    query = ''' 
    prefix owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?subject ?predicate ?object
    WHERE {
      ?subject  owl:description  ?object .
    }
    LIMIT 25 '''
    
    sparql = SPARQLWrapper(url)
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    #print (response)
    results = response['results']['bindings']
    
    print (results)
  
    
except Exception as err:
    print(err)