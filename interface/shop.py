from db.db_handle import db_serialization
from interface.user import get_userinfo_by_name
from lib import  common
from interface import bank

def shopping_interface(name,shopping_card,cost_money):
    '''
    购物接口
    :param name:
    :param shopping_card:
    :param cost_money:
    :return:
    '''
    #需要消费进行扣款，那么这个应该和银行打交道 调用bank接口去做这件事情
    #这个银行的接口要判断我的钱是否大于花费的钱
    #是否扣费成功
    consum_success=bank.consum_interface(name,cost_money)
    if consum_success:
        #保存购物车
        user_dic=get_userinfo_by_name(name)
        user_dic['shopping_card']=shopping_card
        #更新用户json字典
        db_serialization.update(user_dic)
        common.log('%s 花费 %s 购买了 %s' %(name,cost_money,shopping_card))
        print('%s 花费 %s 购买了 %s' %(name,cost_money,shopping_card))
        return True
    else:
        return False
def check_shopping_cart_interface(name):
    user_dic=get_userinfo_by_name(name)
    return user_dic['shopping_card']

