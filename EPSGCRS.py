# -*- coding: utf-8 -*-

import json
import requests

strkey = {"keywords":"ED50 / UTM ZONE 31N"}
siteurl = 'https://apps.epsg.org/api/v1/CoordRefSystem'
headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(siteurl,params=strkey,headers=headers,verify=False)
response.encoding='utf-8'
print(response.status_code)  
#Response as String  
print(response.text)    
#Response as JSON
print(response.json())

#strresponse= response.text
#print(json.loads(strresponse,encoding='utf-8'))

#headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
 #          "content-encoding" : "utf-8",
    #       'Accept-Charset': 'utf-8'}

