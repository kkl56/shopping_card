from msilib.schema import Class
from sqlite3 import dbapi2
import json
import os
from conf import setting


class Serialization:
    # 反序列方法
    def select(self,name):
        print(name)
        # 文件路径定义在setting
        path=r'%s/%s.json'%(setting.DB_path,name)
        if os.path.isfile(path):
            with open(path,'r',encoding='utf-8') as f:
                return json.load(f)

        else:
            return False


    def update(self,user_dic):
        name=user_dic['name']
        path=r'%s/%s.json'%(setting.DB_path,name)
        with open(path,'w',encoding='utf-8') as f:
            json.dump(user_dic,f)
            f.flush()
            #return json.load(f)
db_serialization=Serialization()