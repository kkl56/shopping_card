from lib import common
from interface import  user
from db.db_handle import db_serialization
def check_balance_interface(name):
    user_dic = user.get_userinfo_by_name(name)
    user_account=user_dic['account']
    common.log('%s 查看了余额' %name)
    return user_account

def transfer_interface(from_name,to_name,trans_money):
    '''

    转账接口输入自己name，别人name，和钱
    :param from_name:
    :param to_name:
    :param trans_money:
    :return:
    '''
    from_user_dic=user.get_userinfo_by_name(from_name)
    to_user_dic=user.get_userinfo_by_name(to_name)
    if from_user_dic['account']>=trans_money:
        from_user_dic['account']-=trans_money
        to_user_dic['account']+=trans_money
        #记录流水
        from_user_dic['bankflow'].append('%s 转账%s 圆给 %s' %(from_name,trans_money,to_name))
        to_user_dic['bankflow'].append('%s 收到%s 转账 %s' %(to_name,from_name,trans_money))
        #写入json，更新用户转账数据
        db_serialization.update((from_user_dic))
        db_serialization.update(to_user_dic)
        common.log('%s 收到 %s 转账 %s' %(to_name,from_name,trans_money))
        print('%s 向 %s 转账 %s' %(from_name,to_name,trans_money))
    else:
        print('转账的钱不够')

def repay_interface(name,account):
    '''
    存款接口
    :param name:
    :param account:
    :return:
    '''
    ##查询json用户获取用户字典
    user_dic=db_serialization.select(name)
    user_dic['account']+=account
    #记录流水
    user_dic['bankflow'].append('%s存入%s圆' %(name,account))
    db_serialization.update(user_dic)
    print('%s存款了%s圆' %(name,account))
    common.log('%s存入%s圆' %(name,account))

def withdraw_interface(name,account):
    '''
    取款接口
    :param name:
    :param account:
    :return:
    '''
    ## 查询json用户获取用户字典
    user_dic = db_serialization.select(name)
    #用户字典余额减去取款
    user_dic['account'] -=account
    user_dic['bankflow'].append('%s取出%s圆' %(name,account))
    ## 写入json更新用户存款数据
    db_serialization.update(user_dic)
    print('%s 取出了%s' %(name,account))
    common.log('%s取出了%s' %(name,account))

def consum_interface(name,account):
    '''
    扣费接口
    :param name:
    :param account:
    :return:
    '''
    #查询用户json字典
    user_dic = user.get_userinfo_by_name(name)
    if user_dic['account'] >=account:
        user_dic['account'] -=account
        #添加道bankflow列表里面记录流水
        user_dic['bankflow'].extend(['%s 消费了%s圆钱' %(name,account)])
        #添加道bankflow列表里面记录流水
        db_serialization.update(user_dic)
        common.log('%s 消费了%s圆钱' %(name,account))
        print('%s 消费了%s圆钱' %(name,account))
        return True
    else:
        return False

def lookup_flow_interface(name):
    user_dic=user.get_userinfo_by_name(name)
    common.log('%s 查看了流水' % name)
    return user_dic['bankflow']