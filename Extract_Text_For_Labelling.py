# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 17:27:59 2020

@author: SA20149963
"""

import spacy
import PyPDF2
import io
import os
import json
nlp=spacy.load('en_core_web_sm')
textfilepath = r"D:\OSDU\Unstructured_Data\text_files_extracted_from_pdf"
def load_pdf_document():
    text =''
    count = 0
    source = r"D:\OSDU\Unstructured_Data\prov33.pdf"
    with open(source, "rb") as f:
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(f)
        pagecount = pdfReader.numPages
        #print(pdfReader.numPages)
        while count < pagecount: 
             pageObj = pdfReader.getPage(count)
             text += pageObj.extractText()
             count+=1
    f.close() 
    return text

def extract_sentences_and_create_text_file(pdffilepath):
    filename_with_extention = os.path.basename(pdffilepath).split('.')
    text_filename = filename_with_extention[0] + '.txt'
    MyFile=open(os.path.join(textfilepath,text_filename),'w',  encoding='utf-8')
    textfrompdf = load_pdf_document()
    doc = nlp(textfrompdf)
    sentenses = list(doc.sents)
    for element in sentenses:
        MyFile.write(str(element))
        MyFile.write('\n')
    MyFile.close()
    
    
extract_sentences_and_create_text_file(r"D:\OSDU\Unstructured_Data\prov33.pdf")