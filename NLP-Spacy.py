# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:41:13 2020

@author: SA20149963
"""

import spacy
from spacy import displacy
from spacy.matcher import Matcher



nlp= spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
keyvalue_text = '''company: statoil 
                well: 15/9-F-1 B 
                filed: Volve '''
about_text = ('Gus Proto is a Python developer currently'
               ' working for a London-based Fintech'
               ' company. He is interested in learning'
               ' Natural Language Processing.')
about_interest_text = ('He is interested in learning'
     ' Natural Language Processing.')
piano_class_text = ('Great Piano Academy is situated'
     ' in Mayfair or the City of London and has'
     ' world-class piano instructors.')

#piano_class_doc = nlp(keyvalue_text)
#about_interest_doc = nlp(about_interest_text)
about_doc = nlp(keyvalue_text)
sentences = list (about_doc.sents)

#Break down the content in to sentences
#for sentence in sentences:
  #  print(sentence)
#Tokenize the content from the sentences and index the tokens
#for token in about_doc:
 #   print(token, token.idx, token.is_stop, token.tag_,token.pos_)
'''
displacy.serve(piano_class_doc,style='dep')
for ent in piano_class_doc.ents:
    print(ent.text, ent.start_char, ent.end_char,
          ent.label_, spacy.explain(ent.label_)) '''

def extract_full_name(nlp_doc):
    print(nlp_doc)
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    matcher.add('FULL_NAME', None, pattern)
    matches = matcher(nlp_doc)
    print(matches)
    for match_id, start, end in matches:
         span = nlp_doc[start:end]
         print(span.text)
extract_full_name(about_doc)