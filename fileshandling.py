# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 20:17:28 2020

@author: SA20149963
"""
from neo4j import GraphDatabase
import spacy
import PyPDF2
import requests
import os
import json

nlp= spacy.load('en_core_web_sm')
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))

#Azure Cognitive search 
subscription_key = "9f5b2b36a83c4022ae27fa5ada424468"
endpoint = "https://osdu-cognitive-service.cognitiveservices.azure.com/"
language_api_url = endpoint + "/text/analytics/v3.0/languages"
keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
#end azure cogsearch

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
def create_graphnodes(tx, content, filename):
    #create graph nodes to store pdf content in the 'body' property
    query = '''"""MERGE (log:Welllog{name:"'''+filename+'''", body:"'''+content+'''"}) return log"""'''
    result = tx.run(query)
    for record in result:
      print(record)
#Retrieve the content from PDF file    
pdf_content = get_pdf_content('D:/OSDU/Well_Log_Reports/WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf')

#documents = {'documents':pdf_content}
#body = json.dumps (documents)
#headers = {"Ocp-Apim-Subscription-Key": subscription_key}
#response = requests.post(keyphrase_url,data=body, headers=headers , verify=False)
#languages = response.json()
#print(languages)

#Process the content through NLP pipeline 
#Extract sentenses from the content
content_from_nlp = nlp(pdf_content)
sentences = list (content_from_nlp.sents)
#Tokenize the content from the sentences and index the tokens
#Create a collection of tokens by removing stop words
for ent in content_from_nlp:
    print(ent.text)
content_no_stopword = [token for token in content_from_nlp if not  token.is_stop and not token.is_punct ]
#print(content_no_stopword)

#with driver.session() as session:
 #   session.write_transaction(create_graphnodes,pdf_content.decode(), "WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf")
