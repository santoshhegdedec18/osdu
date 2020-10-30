# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:02:11 2020

@author: SA20149963
"""

import PyPDF2
import textract 

open_filename = open('D:/OSDU/Well_Log_Reports/WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf', 'rb')

pdf_content = PyPDF2.PdfFileReader(open_filename)
print(pdf_content.getDocumentInfo())
total_pages = pdf_content.numPages
count = 0
text  = ''

# Lets loop through, to read each page from the pdf file
while(count < total_pages):
    # Get the specified number of pages in the document
    mani_page  = pdf_content.getPage(count)
    # Process the next page
    count += 1
    # Extract the text from the page
    text += mani_page.extractText()
    if text != '':
        text = text
    else:
        text = textract.process('D:/OSDU/Well_Log_Reports/WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf', method='tesseract', encoding='utf-8', langauge='eng' )

print(text)