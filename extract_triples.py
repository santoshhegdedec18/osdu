# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 20:59:22 2020

@author: SA20149963
"""
import spacy
import PyPDF2

nlp = spacy.load('en_core_web_sm')

def get_pdf_content(filename):
    pdf = open(filename, 'rb')
    # Creating pdf reader object.
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    # Checking total number of pages in a pdf file.
   # print("Document Metadata:", pdf_reader.getDocumentInfo())
    # Creating a page object.
    pages = pdf_reader.numPages
    # Extract data from a specific page number.
    content = ''
   # metadata = pdf_reader.getDocumentInfo()
    for i in range(pages):
        page=pdf_reader.getPage(i)
        content = content + page.extractText().replace("\n","").lower()
    pdf.close()
    return content.encode("ascii",errors='namereplace').decode()

def extract_relations(doc):

    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()
    
    triples = []
        
    for ent in doc.ents:
        preps = [prep for prep in ent.root.head.children if prep.dep_ == "prep"]
        for prep in preps:
            for child in prep.children:
                triples.append((ent.text, "{} {}".format(ent.root.head, prep), child.text))              
    return triples
pdf_content = get_pdf_content(r'D:\OSDU\Unstructured_Data\prov22.pdf')
content_from_nlp = nlp(pdf_content)
sentences = list (content_from_nlp.sents)

for text in sentences:
    print("\n" + str(text))
    relations = extract_relations(nlp(str(text)))
    for r1, r2, r3 in relations:
        print('({}, {}, {}) '.format(r1, r2, r3))
