from interface import user
from interface import bank
import time
from lib.common import login_intter
from interface import  shop
user_data={'name':None,'is_auth':False,}

def login():
    if user_data['is_auth']:
        print('你已登录')
        return

    print('请登录')
    count = 0
    while True:
        name= input('请输入用户名').strip()
        user_dic=user.get_userinfo_by_name(name)
        if user_dic:
            if user_dic['locked']:
                #解锁
                time.sleep(5)
                user.unlock_user(name)
                count=0
                continue
            pwd = input('输入密码').strip()
            print('测试',user_dic['password'])
            print(user_dic,user_dic['locked'])
            if user_dic['password'] == pwd and  user_dic['locked'] == False: #and user
                #用户状态
                user_data['name']=name
                user_data['is_auth']=True
                print('登录成功')
                break
            else:
                print('密码错误')
                count+=1
            if count == 3:
                user.lock_user(name)
                #test
                user_dic=user.get_userinfo_by_name(name)
                print(user_dic)
                print(user_data)
        else:
            print('用户不存在')
def register():

    if user_data['is_auth']:
        print('你已注册')
        return
    print('注册')
    while True:
        name = input('输入用户名').strip()
        #四
        #查看用户是否已经注册需要用到接口interface对应的user
        user_dic = user.get_userinfo_by_name(name)
        #print(user_dic)
        if not  user_dic:
            pwd = input('输入密码').strip()
            pwd1 = input('确认密码').strip()
            if pwd == pwd1:
                user.register_user(name,pwd)
                break
            else:
                print('2次密码不一致')
        else:
            print('用户名已经存在')
@login_intter
def check_balance():
    print('查看余额')
    balance=bank.check_balance_interface(user_data['name'])
    print('你的余额为%s' %balance)
@login_intter
def transfer():
    while True:
        trans_name= input('请输入转入用户名，q返回退出转账').strip()
        if trans_name == user_data['name'] or trans_name == user_data['name'].upper():
            print('不能给自己转账')
            continue
        if 'q' == trans_name:
            break
        trans_dic = user.get_userinfo_by_name(trans_name)
        if trans_dic:
            trans_money = input('输入转账的金额').strip()
            if trans_money.isdigit():
                trans_money=int(trans_money)
                if trans_money > 0:
                    #根据登录名拿到余额
                    user_balance = bank.check_balance_interface(user_data['name'])
                    #用户余额必须大于转入的钱
                    if user_balance > trans_money:
                        #写转账接口 user_data['name']，trans_name,trans_money
                        bank.transfer_interface(user_data['name'],trans_name,trans_money)
                        break
                    else:
                        print('余额不足')

    print('转账')
@login_intter
def repay():
    print('存款')
    while True:
        account = input('请输入存款的金额，输入q退出').strip()
        if account == 'q':break
        if account.isdigit():
            account=int(account)
            if account >0:
                # 调用存款接口执行存款的业务逻辑，传入用户名和存款金额
                bank.repay_interface(user_data['name'],account)
                break
            else:
                print('存款大于0')
        else:print('请输入数字')

@login_intter
def withdraw():
    print('取款')
    while True:
        qukuan_money = input('请输入取款的金额，输入q退出').strip()
        if qukuan_money == 'q':break
        if qukuan_money.isdigit():
            qukuan_money = int(qukuan_money)
            if qukuan_money >0:
                # 余额
                user_account = bank.check_balance_interface(user_data['name'])
                # 取款
                if user_account >= qukuan_money:
                    # 调用取款接口执行取款的业务逻辑，传入用户名和取款金额
                    bank.withdraw_interface(user_data['name'], qukuan_money)
                    print('取款%s圆成功' % qukuan_money)
                    break
                # 调用存款接口执行存款的业务逻辑，传入用户名和存款金额
                bank.repay_interface(user_data['name'],qukuan_money)
                break
            else:
                print('取款金额需要大于0')
        else:
            print('请输入数字')
@login_intter
def check_record():
    print('查看流水')
    record=bank.lookup_flow_interface(user_data['name'])
    print('流水')
    for i in record:
        print(i)
@login_intter
def shopping():
    print('购物')
    goods_list = [
        ['coffee',30],
        ['chicken',20],
        ['iPhone',8000],
        ['macBook',12000],
        ['car',10000]
    ]
    shopping_cart = {}
    # 调用查询余额接口，根据登录名拿到余额
    user_money = bank.check_balance_interface(user_data['name'])
    cost_money = 0
    while True:
        for i,item in enumerate(goods_list):
            print(i,item)
        choice = input('请输入购物编号').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice <0  or  choice >=len(goods_list):continue
            goods_name=goods_list[choice][0]
            goods_price=goods_list[choice][1]
            if user_money >=goods_price:
                if goods_name in shopping_cart:
                    shopping_cart[goods_name]['count']+=1
                    shopping_cart[goods_name]['price']=shopping_cart[goods_name]['count'] *goods_price
                else:
                    shopping_cart[goods_name]={'price':goods_price,'count':1}
                user_money -=goods_price
                cost_money+=goods_price
                print('%s 新的购物商品' %goods_name)
            else:
                print('钱不够')
                continue
        elif choice == 'q':
            print(shopping_cart)
            buy = input('买不买（y/n):').strip()
            if buy == 'y':
                if cost_money == 0:break
                shop_success = shop.shopping_interface(user_data['name'],shopping_cart,cost_money)
                if shop_success:
                    print('购买成功')
                    break
                else:
                    print('钱不够')
                    break
            else:
                print('不买')
                break
        else:
            print('非法输入')


@login_intter
def look_shoppingcart():
    print('查看购物车')
    shopping_cart=shop.check_shopping_cart_interface(user_data['name'])
    print(shopping_cart)
    for i,item in enumerate(shopping_cart):
        print('商品1'+str(i+1),'：',item,' 价格：',shopping_cart[item]['price'],' 数量：',shopping_cart[item]['count'])
def loginout():
    print('注销')
    user_data['is_auth']=False

def run():
    print('开始')

fun_dic={
    '1':login,
    '2':register,
    '3':check_balance,
    '4':transfer,
    '5':repay,
    '6':withdraw,
    '7':check_record,
    '8':shopping,
    '9':look_shoppingcart,
    '10':loginout,
}


def run():
    while True:
        print("""
        '1':登录
        '2':注册
        '3':查看余额
        '4':转账
        '5':存款
        '6':取款
        '7':查看流水
        '8':购物
        '9':查看购买商品
        '10':注销

        """)
        choice=input('输入商品编号').strip()
        if choice not in fun_dic:continue
        fun_dic[choice]()