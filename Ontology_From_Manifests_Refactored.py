# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:33:29 2020

@author: SA20149963
"""

import json
import types

from owlready2 import * 
from owlready import *  


#downloaded json schema files from  https://community.opengroup.org/osdu/platform/open-test-data/-/tree/master/rc--2.0.0
well_file = open('D:\OSDU\Manifest_files\schemas\well\well.json')
wellbore_file = open('D:\OSDU\Manifest_files\schemas\wellbore\wellbore.json')
well_log_file = open('D:\OSDU\Manifest_files\schemas\welllog\WorkProduct.json')

#Load json schema files and create a dictonary object using json package
well_json_data = json.load(well_file)
wellbore_json_data = json.load(wellbore_file)
well_log_json_data = json.load(well_log_file)

#Close all open file object
well_file.close()
wellbore_file.close()
well_log_file.close()

#Load Ontology .owl file through file URI, the method can also create a new file if not exists already
#Create base class to connect all WELL objects using owlready package

uri = r"http://osdu_vocab" 


osdu_onto = get_ontology(uri)


class Well(Thing):
    ontology = osdu_onto
    
class Wellbore(Well):
    ontology = osdu_onto
    
class Well_Log(Wellbore):
    ontology = osdu_onto

#my_ind = WELL("well_500")  
#Lists declared to ignore some of the properties and group headers that are not important for creating ontology
props_tobe_ignored = ["type", "pattern", "format", "$ref"]
headers_tobe_ignored = ["ExtensionProperties","properties", "GroupTypeProperties","IndividualTypeProperties","allOf","items", "Data","ID","RelationshipType"]

#Class to initiate WELL class creation using the json dictionary object
def create_well_annotations(class_well):
    ANNOTATIONS[class_well].add_annotation("comment", "WELL Class defines the attributes and properties of well json manifest schema")
    ANNOTATIONS[class_well].add_annotation("label", "WELL")
    ontology_creation_orchestrator(well_json_data, class_well)
    close_world(class_well)

#Class to initiate WELLBORE class creation using the json dictionary object
def create_wellbore_annotations(class_wellbore):
    ANNOTATIONS[class_wellbore].add_annotation("comment", "WELLBORE Class defines the attributes and properties of wellbore json manifest schema")
    ANNOTATIONS[class_wellbore].add_annotation("label", "WELLBORE")
    ontology_creation_orchestrator(wellbore_json_data, class_wellbore)
    close_world(class_wellbore)

#Class to initiate WELLLOG OR WORKPRODUCT class creation using the json dictionary object    
def create_well_log_annotations(class_well_log):
    ANNOTATIONS[class_well_log].add_annotation("comment", "WELL LOG Class defines the attributes and properties of work product json manifest")
    ANNOTATIONS[class_well_log].add_annotation("label", "WELL LOG")
    ANNOTATIONS[class_well_log].add_annotation("label", "WORK PRODUCT")
    ANNOTATIONS[class_well_log].add_annotation("label", "WELLLOG")
    ontology_creation_orchestrator(well_log_json_data, class_well_log)
    close_world(class_well_log)

# Function to anchor class creation process, recursively call appropriate methods untill all the levels 
# in the input jsonv dictionary objet is exhausted. dictionaly object might contain list objects inside as well
def ontology_creation_orchestrator(json_data, ontoclass):
    #print("in..............ontology_creation_orchestrator")
    if isinstance(json_data, dict):
        handle_dictionary_object(json_data, ontoclass)
    elif isinstance(json_data, list):
        handle_list_object(json_data, ontoclass)
    else:
        #handle_single_dictionary_element(json_data,json_data, ontoclass)
        print("Single element with key, value..... %",json_data, type(json_data))

# Method is called to handle a sub dictionary object from a parent dictionary recursively
def handle_dictionary_object(dic, ontoclass):
    for key, value in dic.items():
        if not type(value) == bool and isinstance(value, dict):
            cls_obj = handle_group_headers(key, ontoclass)
            ontology_creation_orchestrator(value, cls_obj)
        elif not type(value) == bool and isinstance(value, list):
           handle_list_object(key, value, ontoclass)
        else:
            handle_single_dictionary_element(key, value, ontoclass)

# Method is called to create annotation properties and assign to the parent class recursively 
def handle_single_dictionary_element(key, value, ontoclass):
    if key not in props_tobe_ignored:
        annot_prop=types.new_class(key,(AnnotationProperty,),kwds=None)
        ANNOTATIONS[ontoclass].add_annotation(annot_prop,value)
        annot_label=types.new_class("label",(AnnotationProperty,),kwds=None)
        ANNOTATIONS[ontoclass].add_annotation(annot_label,key.replace('ID',''))

#Method is called to create classes from a list object recursively
def handle_list_object(key, lst, ontoclass):
    for item in lst:
        if isinstance(item,list):
            class_lst = types.new_class(key,(ontoclass,),kwds=None)
            annot_prop=types.new_class("label",(AnnotationProperty,),kwds=None)
            ANNOTATIONS[class_lst].add_annotation(annot_prop,item.replace('ID',''))
        else:
            ontology_creation_orchestrator(item, ontoclass)


# Method called to create sub class for the group headers whenever required
def handle_group_headers(key, ontoclass):
    if key not in headers_tobe_ignored:
        class_obj = types.new_class(key,(ontoclass,),kwds=None)
        annot_prop=types.new_class("label",(AnnotationProperty,),kwds=None)
        ANNOTATIONS[class_obj ].add_annotation(annot_prop,key.replace('ID',''))
        osdu_onto.add(class_obj)
        ontoclass = class_obj
        
        
        
    return ontoclass


create_well_annotations(osdu_onto.Well) 
create_wellbore_annotations(osdu_onto.Wellbore)
create_well_log_annotations(osdu_onto.Well_Log)
osdu_onto.save('D:/OSDU/Ontology/Wells_Ontology_rdf.owl')





    


