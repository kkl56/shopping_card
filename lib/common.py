import time
from core import src
from conf import setting


def log(msg):
    current_time = time.strftime('%Y-%m-%d %X')
    with open(setting.LOG1_path,'a',encoding='utf-8') as f:
        f.write(current_time + '-' *5 +msg+'\n')
        f.flush()

def login_intter(func):
    def wrapper():
        if not src.user_data['is_auth']:
            src.login()
        else:
            func()
    return wrapper