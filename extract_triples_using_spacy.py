# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 15:17:25 2020

@author: SA20149963
"""

import spacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
nlp = spacy.load('en_core_web_sm')
source_file = r"D:\OSDU\Unstructured_Data\text_files_extracted_from_pdf\prov22.txt"
csv_path = r'D:\OSDU\Unstructured_Data\triples_csv'
csv_columns = ['subject','object','predicate']
def load_text_document(source_file):
     
     text = open(source_file, "r",  encoding='utf-8').read()
     return text

def get_entities(sent):
    # chunk 1
    ent1 = ""
    ent2 = ""
    prv_tok_dep = ""    # dependency tag of previous token in the sentence
    prv_tok_text = ""   # previous token in the sentence
    prefix = ""
    modifier = ""
    
    ##################################################
    for tok in nlp(sent):
        #Chunk 2
        # if token is a punctuation mark then move on to the next token
        if tok.dep_ != "punct":
            # check: token is a compound word or not
            if tok.dep_ == "compound":
                prefix = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    prefix = prv_tok_text + " "+ tok.text
            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " "+ tok.text
            
            #Chunk 3
            if tok.dep_.find("subj") == True:
                ent1 = modifier +" "+ prefix + " "+ tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = "" 
            ## chunk 4
            if tok.dep_.find("obj") == True:
                 ent2 = modifier +" "+ prefix +" "+ tok.text
    
            ## chunk 5
            # update variables
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text
    return {'subject':ent1.strip(),'object': ent2.strip()}

def get_relation(sent):
    doc = nlp(sent)
    # Matcher class object 
    matcher = Matcher(nlp.vocab)
    #define the pattern 
    pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}]
    matcher.add("matching_1", None, pattern)
    matches = matcher(doc)
    k = len(matches) - 1
    span = doc[matches[k][1]:matches[k][2]]
    return(span.text)

def generate_csv_file(filename, path, csv_columns, list_data):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        csv_file = os.path.join(path,filename)
        with open(csv_file, 'w', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in list_data:
                writer.writerow(data)
    except IOError as e:
        print(str(e))


content = load_text_document(source_file)
doc = nlp (content)
sents = list (doc.sents)

entities = []

for sent in sents:
    triples = get_entities(str(sent))
    relations = get_relation(str(sent))
    triples_dict = {}
    if triples["subject"] != "" and  triples["object"] != "" and relations != "":
        triples_dict['subject'] = triples['subject']
        triples_dict['object'] = triples['object']
        triples_dict['predicate'] = relations
        entities.append (triples_dict)

def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple["subject"])
        G.add_node(triple["object"])
        G.add_node(triple["predicate"])
        G.add_edge(triple["subject"], triple["predicate"])
        G.add_edge(triple["predicate"], triple["object"])
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='skyblue', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()
#print(entities)
#printGraph(entities)
filename = os.path.basename (source_file)
filename = os.path.splitext(filename)[0] + ".csv"
generate_csv_file(filename,csv_path,csv_columns, entities )  



