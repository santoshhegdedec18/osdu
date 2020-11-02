# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 21:09:15 2020

@author: SA20149963
"""
# import the neo4j driver for Python
#uri             = "bolt://20.185.241.225:7687"
from neo4j import GraphDatabase
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))

def get_friends_of(tx):
    friends = []
    result = tx.run("MATCH (n:Resource) return count(n) as node ")
    for record in result:
        friends.append(record["node"])
    return friends

def delete_all_nodes(tx):
    #delete all the nodes and relationships
    result = tx.run("match(n:Resource) detach delete n")
    for record in result:
       print(record)

def initiate_neosemantics(tx):
    #initiate the neosemantics graph config to handle lisy of labels as synonyms
    result = tx.run("CALL n10s.graphconfig.init({ keepLangTag: true, handleMultival: 'ARRAY'})")
    print("\n Instantiated the Graph config...........\n")
    for record in result:
       print(record)
    print("Completed Instantiating...........\n")

def create_constraint(tx):
    #initiate the neosemantics graph config to handle lisy of labels as synonyms
    result = tx.run("CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS  ON (r:Resource) ASSERT r.uri IS UNIQUE")
    print("\n Created Constraint...........\n")
    for record in result:
       print(record)
    print("Completed creating constraint...........\n")
    
def import_ontology(tx):
    #import Ontology using neosemantics plugin
    result = tx.run("CALL n10s.rdf.import.fetch('file:///home/osdugraph/datashare/test.owl','Turtle')")
    print("Imported the Ontology...........\n")
    for record in result:
       print(record)
    print("Completed Importing the Ontology...........\n")
        
#Call the function to display number of nodes in the graph
with driver.session() as session:
    friends = session.read_transaction(get_friends_of)
    print("Total number of nodes before deleting..")
    for friend in friends:
        print(friend)
#Call the function to delete all nodes and relationships
with driver.session() as session:
    session.write_transaction(delete_all_nodes)
#Call the function to display the count of nodes after deleting, should be "0"
with driver.session() as session:
    friends = session.read_transaction(get_friends_of)
    print("Total number of nodes after deleting..,,")
    for friend in friends:
        print(friend)
#Call the function to initialize graph
with driver.session() as session:    
    session.write_transaction(initiate_neosemantics)

#Call the function to create constraint
with driver.session() as session:    
    session.write_transaction(create_constraint)

#import Ontology using neosemantics plugin / import ontology OWL file
with driver.session() as session:    
    session.write_transaction(import_ontology)

#count the number of nodes after inporting the ontology
with driver.session() as session:
    friends = session.read_transaction(get_friends_of)
    print("Total number of nodes after importing Ontology..,,")
    for friend in friends:
        print(friend)
  
driver.close()