# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 10:41:03 2020

@author: SA20149963
"""
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.models import Model 
import bert
from bert import bert_tokenization

input_sentence= 'Hi we are using BERT'
FullTokenizer = bert.bert_tokenization.FullTokenizer # install : pip install bert-for-tf2
#BERT architectureconfig
max_seq_length = 128 
input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
 name="input_word_ids")
input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
 name="input_mask")
segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
 name="segment_ids")
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1",
 trainable=True)
pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=[pooled_output, sequence_output])

# See BERT paper: https://arxiv.org/pdf/1810.04805.pdf
# And BERT implementation convert_single_example() at https://github.com/google-research/bert/blob/master/run_classifier.py

def get_masks(tokens, max_seq_length):
    """Mask for padding"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    return [1]*len(tokens) + [0] * (max_seq_length - len(tokens))


def get_segments(tokens, max_seq_length):
    """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))


def get_ids(tokens, tokenizer, max_seq_length):
    """Token ids from Tokenizer vocab"""
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = token_ids + [0] * (max_seq_length-len(token_ids))
    return input_ids

vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = FullTokenizer(vocab_file, do_lower_case)

s = '''SAN JUAN BASIN PROVINCE (022)•By A. Curtis Huffman, Jr. INTRODUCTION
The San Juan Basin province incorporates much of the area from latitude 35û to 38û N. and from longitude 106û to 109û W. and comprises all or parts of four counties in northwest New Mexico and six counties in southwestern Colorado.'''
stokens = tokenizer.tokenize(s)
stokens = ["[CLS]"] + stokens + ["[SEP]"]

input_ids = get_ids(stokens, tokenizer, max_seq_length)
input_masks = get_masks(stokens, max_seq_length)
input_segments = get_segments(stokens, max_seq_length)

print(stokens)

for i in stokens:
    print(i.pos)

#print(input_ids)
#print(input_masks)
#print(input_segments)

#pool_embs, all_embs = model.predict([[input_ids],[input_masks],[input_segments]])