# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:53:51 2020

@author: SA20149963
"""

import spacy
import io
model_dir = 'D:/OSDU/AI Models'
nlp=spacy.load(model_dir)

def load_text_document():
       source = r"D:\OSDU\Unstructured_Data\text_files_extracted_from_pdf\prov33.txt"
       text = open(source, "r",  encoding='utf-8').read()
       #print (text)
       return text
    
doc = nlp(load_text_document())
print(doc.ents)
for ent in doc.ents:
    print(ent.text, ent.label_)

