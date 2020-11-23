# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:42:39 2020

@author: SA20149963
"""

import sys
import elasticsearch
import requests

auth_token = '''eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCIsImtpZCI6ImtnMkxZczJUMENUaklmajRydDZKSXluZW4zOCJ9.eyJhdWQiOiI0MTY1M2VjNC1kNjEzLTQ3OWYtOTY2YS1lNTdlZTg2Mzk1N2MiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82MTBkZmFkYy1lMjMyLTRmOWQtOTc4ZS1lYjI5YjFiYWYwMzYvIiwiaWF0IjoxNjAxOTgzNTkxLCJuYmYiOjE2MDE5ODM1OTEsImV4cCI6MTYwMTk4NzQ5MSwiYWNyIjoiMSIsImFpbyI6IkFVUUF1LzhSQUFBQUtZUjk5WDgzTTJnNVU4clkxWFBKcHpDdXFVZFhnR2JRa0VMeURzRFcvR1NKaVFnK3BMZGtzeUw0TUVYY1VmazExa1lDdUhWc0NKN0ltWE4xSktKK0JRPT0iLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiNDE2NTNlYzQtZDYxMy00NzlmLTk2NmEtZTU3ZWU4NjM5NTdjIiwiYXBwaWRhY3IiOiIxIiwiZW1haWwiOiJzYW50YW51Lm1hamkxQHdpcHJvLmNvbSIsImZhbWlseV9uYW1lIjoibWFqaSIsImdpdmVuX25hbWUiOiJzYW50YW51IiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMjU4YWM0ZTQtMTQ2YS00MTFlLTlkYzgtNzlhOWUxMmZkNmRhLyIsImlwYWRkciI6IjE2NS4yMjUuMTA0LjgwIiwibmFtZSI6InNhbnRhbnUgbWFqaSIsIm9pZCI6ImI0MGE0YjBkLTc1YzEtNGNiYy04MTU3LWIwZDkwYTI3NTNjNyIsInJoIjoiMC5BVGdBM1BvTllUTGluVS1YanVzcHNicndOc1EtWlVFVDFwOUhsbXJsZnVoamxYdzRBSEkuIiwic2NwIjoiVXNlci5SZWFkIiwic3ViIjoiQndaYlhoVUNRQm9Ld3dzbERucmFzVEVnZnpickdHSld0aFcybUhtUlV5TSIsInRpZCI6IjYxMGRmYWRjLWUyMzItNGY5ZC05NzhlLWViMjliMWJhZjAzNiIsInVuaXF1ZV9uYW1lIjoic2FudGFudS5tYWppMUB3aXByby5jb20iLCJ1dGkiOiJVYjIzbzM0bWhFNlpmSVF0YU5VTkFBIiwidmVyIjoiMS4wIn0.OzoMFYRubUz2dgQkzZonWXaCoI5oxWQqKOmQD9PSjdnPtyyI9SzDZjWDwY7KWIUhmAI9e4UNmgR8luq-yGpz5LwRh63LiWtD4VDH5rqJ_aZoBUug-FC1XiXtTGMXeFP6se2BH0NMswhaMplzju2pGlWllEOUR_tJQ_IC01NUgiQmCAm31Xihgkzg2JZrhnfd81sP9DVQZXMyuJDbDwPXZWattwmHU2ZLZ8ufyOjKrcXgVZKk7DOvwEoUuMHMBqbr_0sslB3tLAkvbuW5W8lspCqyXpc5OIQte1USlssbb3hAc3g0LfAQEB7fA07HDeW6DBFKY8zmwgFJXZGe-N_cqA'''
head = head = {
'Content-Type' : 'application/json; charset=utf8',
'Authorization' : 'Basic %s' % auth_token,
'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
}

try:
    res = requests.get('''http://ado-devr2-jo-jorx7l4o-au-search.azurewebsites.net/api/search/v2''', head)
    print(res.json())
except Exception as error:
    print(error)
    