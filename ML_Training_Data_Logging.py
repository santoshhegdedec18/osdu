# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:52:44 2020

@author: SA20149963
"""

import io
import os
from datetime import datetime
class LogManager:
     
     def __init__(self, source, data): 
        self.source = source
        self.data = data
        self.log_file_path = r'''\OSDU\ML Logs'''
     
     def log_data (self):
         now = datetime.now()
         timestamp = datetime.timestamp(now)
         MyFile=open(os.path.join(self.log_file_path,self.source + '_'+ str(timestamp)+ ".txt"),'w',  encoding='utf-8')
         MyFile.write(str(self.data))
         MyFile.close()