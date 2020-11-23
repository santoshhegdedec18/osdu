# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:34:11 2020

@author: SA20149963
"""
import tika # to extract text content form documents
import tabula # to extract tables inside documents OR Camelot
from tabula import read_pdf  # to extract tables from pdf
import spacy # to extract symantics from the text content
import fitz # PyMuPDF, to extract images from pdf document
from PIL import Image # pillow for image encoding
import io
tika.initVM()
from tika import parser
doc_path = r'D:\OSDU\Unstructured_Data\prov22.pdf'
nlp=spacy.load("en_core_web_sm")
nlp_custom_ner = spacy.load('D:\OSDU\AI Models')
doc_content = {'metadata': {}, 'content':{}, 'entities':{}, 'tokens': {}, 'sentenses':{}, 'images':{}, 'tables':{}, 'custom_entities':{}}

def parse_document_from_tika():
    parsed_pdf = parser.from_file(doc_path)
    return parsed_pdf

def extract_entities_from_documents(parsed_pdf):
    doc = nlp(parsed_pdf['content'])
    doc_trained = nlp_custom_ner(parsed_pdf['content'])
    tokens = [token.text for token in doc if token.is_stop == False and token.text.isalpha() == True]
    entities = [(i, i.label_,i.label) for i in doc.ents]
    custom_entities =  [(i, i.label_) for i in doc_trained.ents]
    sentenses = [sent for sent in doc.sents]
    tables = extract_tables_from_pdf_documents(doc_path)
    doc_images = extract_images_from_documents(doc_path)
    doc_content.update ({'metadata': parsed_pdf['metadata'], 'content': parsed_pdf['content'], 'entities': entities,
                     'tokens': tokens, 'sentenses': sentenses, 'tables': tables, 'images':doc_images, 'custom_entities':custom_entities})
    print (custom_entities)
def extract_tables_from_pdf_documents(doc_path):
    tables = read_pdf(doc_path, pages= 'all')
    #uncomment the below line to save the extracted tables as csv file
    tabula.convert_into(doc_path, 'test.csv', output_format='csv', pages='all')
    return tables

def extract_images_from_documents(doc_path):
    doc_images = []
    
    pdf_file = fitz.open(doc_path)
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # uncomment the below line to save it to local disk
            #image.save(open(f'''D:/OSDU/Unstructured_Data/pdf_images/image{page_index+1}_{image_index}.{image_ext}''', "wb"))
            doc_images.append( base_image)
    return doc_images
extract_entities_from_documents(parse_document_from_tika())