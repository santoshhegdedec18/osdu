# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 22:34:23 2020

@author: SA20149963
"""
import spacy
import PyPDF2
import io
import json
import ML_Training_Data_Logging
nlp=spacy.load('en_core_web_sm')

class label_data:
    
    def __init__(self, source): 
        self.source = source
        
    
    def load_pdf_document(self):
        text =''
        count = 0
        source = r"D:\OSDU\Unstructured_Data\prov22.pdf"
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
        #print(text)
    
    def load_text_document(self):
        source = r"D:\OSDU\Unstructured_Data\prov22.txt"
        text = open(source, "r",  encoding='utf-8').read()
        #print(text)
        txt = ""
        #txt = txt.join(text)
        doc = nlp(text)
        sentences = list(doc.sents)
       
        return sentences
    
    def prepare_training_data_from_webanno_output( self, filename):
        # Read output json file from WebAnno (Annotation tool)
        with open(r'''D:\OSDU\Unstructured_Data\training_data\prov22.json''', 'r',encoding='utf-8' ) as data_file:    
            data = json.load(data_file)
            
            # Extract original sentences
            sentences_list = data['_referenced_fss']['12']['sofaString'].split('\n')
            print(len(sentences_list))
            #sentences_list = self.load_text_document()
            #print(len(sentences_list))
            # Extract entity start/ end positions and names
            ent_loc = data['_views']['_InitialView']['SubsurfaceEntities']
            #print(ent_loc)
            # Extract Sentence start/ end positions
            Sentence = data['_views']['_InitialView']['Sentence']
            # Set first sentence starting position 0
            Sentence[0]['begin'] = 0
            # Prepare spacy formatted training data
            TRAIN_DATA = []
            ent_list = []
            #print(len(Sentence))
            for sl in range(len(Sentence)):
                ent_list_sen = []
                for el in range(len(ent_loc)):
                    if(ent_loc[el]['begin'] >= Sentence[sl]['begin'] and ent_loc[el]['end'] <= Sentence[sl]['end']):
                        ## Need to subtract entity location with sentence begining as webanno generate data by treating document as a whole
                        ent_list_sen.append([(ent_loc[el]['begin']-Sentence[sl]['begin']),(ent_loc[el]['end']-Sentence[sl]['begin']),ent_loc[el]['value']])
                ent_list.append(ent_list_sen)
                ## Create blank dictionary
                ent_dic = {}
                ## Fill value to the dictionary
                ent_dic['entities'] = ent_list[-1]
                ## Prepare final training data
                TRAIN_DATA.append([sentences_list[sl],ent_dic])
            
            logger = ML_Training_Data_Logging.LogManager("training_data", TRAIN_DATA )
            logger.log_data()
            return TRAIN_DATA
    prepare_training_data_from_webanno_output("","")
   
