# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:15:54 2020

@author: SA20149963
"""

import spacy
import random
from spacy.util import minibatch, compounding
from pathlib import Path
import NLP_data_labelling
import ML_Training_Data_Logging
# Define output folder to save new model
model_dir = 'D:/OSDU/AI Models'

# Train new NER model

def train_new_NER(model=None, output_dir=model_dir, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")
    
    # add labels
    labeldata = NLP_data_labelling.label_data("")
    TRAIN_DATA =  labeldata.prepare_training_data_from_webanno_output("")
    #print(TRAIN_DATA)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
           ner.add_label(ent[2])
           
    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        #optimizer = nlp.begin_training()
        if model is None:
            optimizer = nlp.begin_training() 
        for itn in range(n_iter):
            
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                logger = ML_Training_Data_Logging.LogManager("batch_data", batch )
                logger.log_data()
                '''
                try:
                    
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.5,  # dropout - make it harder to memorise data
                        sgd=optimizer, #callable to update weights
                        losses=losses,
                    ) 
                except Exception as error:
                    print(error)'''
                    #continue
            '''for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text], #batches of text
                    [annotations], #batch of annotations
                    drop = 0.2, #dropout
                    sgd=optimizer, #callable to update weights
                    losses=losses)'''
            print("Losses", losses)
        # test the trained model
        
        #for text, _ in TRAIN_DATA:
                       
            #doc = nlp(text)
            #print("Entities", [(str(ent.text), str(ent.label_)) for ent in doc.ents])
            #print("Tokens", [(str(t.text), str(t.ent_type_), str(t.ent_iob)) for t in doc])
        # save model to output directory
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            nlp.to_disk(output_dir)
            print("Saved model to", output_dir)
    
            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            for text, _ in TRAIN_DATA:
                doc = nlp2(text)
                print("Entities", [(str(ent.text), str(ent.label_)) for ent in doc.ents])
                print("Tokens", [(str(t.text), str(t.ent_type_), str(t.ent_iob)) for t in doc])
            # Finally train the model by calling above function
train_new_NER()