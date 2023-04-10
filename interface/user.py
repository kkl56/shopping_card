from db.db_handle import db_serialization
from lib import common
def get_userinfo_by_name(name):
    #这里需要用到一个db下面的db_balance 数据管理的方法在这个文件夹下
    #这里需要返回用户信息
    return db_serialization.select(name)
def unlock_user(name):
    user_dic=db_serialization.select(name)
    user_dic['locked']=False
    db_serialization.update(user_dic)
    print('已经解锁')
    common.log('已经解锁')

def lock_user(name):
    user_dic=db_serialization.select(name)
    user_dic['locked']=True
    db_serialization.update(user_dic)
    print('已被锁定')
    #记录日志
    common.log('已被锁定')

def register_user(name,password,balance=15000):
    user_dic = {'name':name,
                'password':password ,
                'locked':False,
                'account':balance,
                'shopping_cart':{},
                'bankflow':[]
                }
    db_serialization.update(user_dic)
    print('%s注册了'%name)
    common.log('%s注册了' %name)
