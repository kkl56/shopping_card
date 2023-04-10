
import json
import os
import sys

cwd=os.getcwd()
print(cwd)
print(cwd+'\李老师.json')
user_dic={'name':'李老师','password':'123','locked':False,'account':15000,'shopping_card':{},'bankflow':[]}
with open(cwd+'\李老师.json','w',encoding='utf-8') as f :
    json.dump(user_dic,f)
    f.flush()