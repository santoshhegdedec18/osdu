# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 19:11:02 2020

@author: SA20149963
"""

import urllib.request
import urllib.response
import sys
import os, glob
import tika
tika.initVM()
from tika import parser
import http.client, urllib
import json
import re

def parsePDF(path):
    documents = { 'documents': []}
    count = 1
    for file in glob.glob(path):
        parsedPDF = parser.from_file(file)
        text = parsedPDF["content"]
        text = text.strip('\n')
        text = text.encode('ascii','ignore').decode('ascii')
        documents.setdefault('documents').append({"language":"en","id":str(count),"text":text})
        count+= 1
    return documents 
# Replace the accessKey string value with your valid access key.
accessKey = '9f5b2b36a83c4022ae27fa5ada424468'
url = 'https://osdu-cognitive-service.cognitiveservices.azure.com/'
path = "/text/analytics/v3.0/keyphrases"

def TextAnalytics(documents):
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection(url)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()
docs = parsePDF("D:/OSDU/Well_Log_Reports/WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf")
print(docs)
print()
print ('Please wait a moment for the results to appear.\n')
result = TextAnalytics (docs)
print (json.dumps(json.loads(result), indent=4))