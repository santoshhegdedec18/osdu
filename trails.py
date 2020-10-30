import re
#text = textract.parsers.pdf_parser('D:/OSDU/Well_Log_Reports/WL_RAW_PROD_CCL-PERF_2013-12-22_PLOT_1.pdf')
#print(text)

text = "Horizontal:srn:reference-data/HorizontalCRS:UTM31_ED50:"

substr = re.match(r"[^a-z]+", text)

print(substr)