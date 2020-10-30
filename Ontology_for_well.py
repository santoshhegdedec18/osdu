import json
import types
from owlready import *

well_file = open('D:\OSDU\Manifest_files\well\load_well_1000.json')
wellbore_file = open('D:\OSDU\Manifest_files\wellbore\load_wellbore_1000.json')
well_log_file = open('D:\OSDU\Manifest_files\welllog\load_log_1013_akm11_1978_comp_las.json')

well_json_data = json.load(well_file)
wellbore_json_data = json.load(wellbore_file)
well_log_json_data = json.load(well_log_file)

well_file.close()
wellbore_file.close()
well_log_file.close()

osdu_onto = get_ontology("file:///D:/OSDU/Ontology/odsu_onto.owl" )
baseclass = types.new_class("WELLS",(Thing,),kwds=None)
osdu_onto.add(baseclass)

ANNOTATIONS[baseclass].add_annotation("comment", "This is a base class for defining ontology for subsurface")
ANNOTATIONS[baseclass].add_annotation("label", "WELLS")
ANNOTATIONS[baseclass].add_annotation("label", "borehole")

class_well = types.new_class("WELL",(baseclass,),kwds=None)
class_wellbore = types.new_class("WELLBORE",(class_well,),kwds=None)
class_well_log = types.new_class("WELL_LOG",(class_wellbore,),kwds=None)

def create_well_class():
    ANNOTATIONS[class_well].add_annotation("comment", "WELL Class defines the attributes and properties of well json manifest")
    ANNOTATIONS[class_well].add_annotation("label", "WELL")
    for mykey,value in well_json_data.items():
        if not isinstance(value,dict):
            create_onto_for_nondict_elements(mykey, value,class_well)
        else:
            print(mykey + " is a dictionary")
            create_onto_for_dict_object(mykey, value, class_well)
            osdu_onto.add(class_well)

def create_wellbore_class():
    ANNOTATIONS[class_wellbore].add_annotation("comment", "WELLBORE Class defines the attributes and properties of wellbore json manifest")
    ANNOTATIONS[class_wellbore].add_annotation("label", "WELLBORE")
    for mykey,value in wellbore_json_data.items():
        if not isinstance(value,dict):
            create_onto_for_nondict_elements(mykey, value,class_wellbore)
        else:
            print(mykey + " is a dictionary")
            create_onto_for_dict_object(mykey, value, class_wellbore)
            osdu_onto.add(class_wellbore)

def create_well_log_class():
    ANNOTATIONS[class_well_log].add_annotation("comment", "WELL LOG Class defines the attributes and properties of well log json manifest")
    ANNOTATIONS[class_well_log].add_annotation("label", "WELL LOG")
    for mykey,value in well_log_json_data.items():
        if not isinstance(value,dict):
            create_onto_for_nondict_elements(mykey, value,class_well_log)
        else:
            #print(mykey + " is a dictionary")
            create_onto_for_dict_object(mykey, value, class_well_log)
            osdu_onto.add(class_well_log)
            
def create_onto_for_list_object(key, value, ontoclass):
    for lst in value:
      if isinstance(lst,list):
          if len(lst)>1:
              print("list agin*****************************")
              create_onto_for_dict_object(key, lst, ontoclass)
          else:
              print("exception")
              
              #print(lst(0])
              #for i in range(0,len(lst)):
                  
                  #annot_prop=types.new_class(k,(AnnotationProperty,),kwds=None)
                  #RANNOTATIONS[ontoclass].add_annotation(annot_prop,value)
      elif isinstance(lst,dict):
          create_onto_for_dict_object(key, value, ontoclass)
      else:
          create_onto_for_nondict_elements(key, value, ontoclass)
          
def create_onto_for_nondict_elements(key, value, ontoclass):
    if isinstance(value,list):
        create_onto_for_list_object(key, value, ontoclass)
    else:
        annot_prop=types.new_class(key,(AnnotationProperty,),kwds=None)
        ANNOTATIONS[ontoclass].add_annotation(annot_prop,value)

def create_onto_for_dict_object(key, value, ontoclass):
    #print(key, ":", value)
    if isinstance(value, dict):
        for k,v in value.items():
            if not isinstance(v,dict):
                #print(k + " is a not dictionary")
                create_onto_for_nondict_elements(k, v, ontoclass)
            else:
                #print(k + " is a dictionary")
                create_onto_for_dict_object(k, v, ontoclass)
    else:
        create_onto_for_list_object(key, value, ontoclass)
        
create_well_class() 
create_wellbore_class()
create_well_log_class()

osdu_onto.save('D:/OSDU/Ontology/odsu_onto.owl')




    


