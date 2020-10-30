# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:01:46 2020

@author: SA20149963
"""

import requests
import os
subscription_key = "9f5b2b36a83c4022ae27fa5ada424468"
endpoint = "https://osdu-cognitive-service.cognitiveservices.azure.com/"
language_api_url = endpoint + "/text/analytics/v3.0/languages"
keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

lang_documents = {"documents": [
    {"id": "1", "text": "This is a document written in English."},
    {"id": "2", "text": "Este es un document escrito en Español."},
    {"id": "3", "text": "这是一个用中文写的文件"}
]}
phrase_documents = {"documents": [
    {"id": "1", "language": "en",
        "text": "I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable."},
    {"id": "2", "language": "es",
        "text": "Si usted quiere comunicarse con Carlos, usted debe de llamarlo a su telefono movil. Carlos es muy responsable, pero necesita recibir una notificacion si hay algun problema."},
    {"id": "3", "language": "en",
        "text": "The Grand Hotel is a new hotel in the center of Seattle. It earned 5 stars in my review, and has the classiest decor I've ever seen."}
]}

senti_documents = {"documents": [
    {"id": "1", "language": "en",
        "text": "I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable."},
    {"id": "2", "language": "es",
        "text": "Este ha sido un dia terrible, llegué tarde al trabajo debido a un accidente automobilistico."}
]}

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(keyphrase_url,json=documents, headers=headers , verify=False)
languages = response.json()
print(languages)