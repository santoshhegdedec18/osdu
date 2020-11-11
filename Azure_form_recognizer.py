# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 20:24:42 2020

@author: SA20149963
"""

import json
import time
from requests import get, post
endpoint = r"https://osdu-form-recognizer.cognitiveservices.azure.com/"
apim_key = "c9a8a7d10b804fe0908cd478fdea24cd"
post_url = endpoint + "formrecognizer/v2.0/prebuilt/receipt/analyze"
source = r"D:\OSDU\Manifest_files\instances\well\master-data_Well_instance_1000.json"

headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': apim_key,
    }
params = {
        "includeTextDetails": True
    }
with open(source, "rb") as f:
        data_bytes = f.read()
        #print(data_bytes)

try:
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        for record in resp:
            print(record)
        if resp.status_code != 202:
            print("POST analyze failed:\n%s" % resp.text)
            quit()
        print("POST analyze succeeded:\n%s" % resp.headers)
       # resp_json = json.loads(resp.text)
        #print(resp_json)
        get_url = resp.headers["operation-location"]
        print(get_url)
except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        #quit()

n_tries = 10
n_try = 0
wait_sec = 6
while n_try < n_tries:
    try:
        resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
        resp_json = json.loads(resp.text)
        if resp.status_code != 200:
            print("GET Receipt results failed:\n%s" % resp_json)
            #quit()
        status = resp_json["status"]
        if status == "succeeded":
            print("Receipt Analysis succeeded:\n%s" % resp_json)
            #quit()
        if status == "failed":
            print("Analysis failed:\n%s" % resp_json)
            #quit()
        # Analysis still running. Wait and retry.
        time.sleep(wait_sec)
        n_try += 1     
    except Exception as e:
        msg = "GET analyze results failed:\n%s" % str(e)
        print(msg)
        #quit()
