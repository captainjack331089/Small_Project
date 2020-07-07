"""
利用装饰器，创建一个简单的登录系统
"""
import re

def register():
    user_dict = {'Jack':None, 'Tom':None}
    while True:
        print('Welcome to Register!')
        username = input('Please Enter Username:: ').strip()
        if username in user_dict:
            print('The username you entered has already been registered \n')
        elif not re.match('^[A-Za-z0-9]*$', username):
            print('The username you entered is not match num/alpha format \n')
        else:
            password = input('Please Enter Password: ').strip()
            confirm_password = input('Please confirm your password: ').strip()
            while confirm_password != password:
                confirm_password = input('password is not correct \nPlease confirm your password: ').strip()
            user_dict[username] = password
            add_new = input('Do you want to register a new one?')
            if add_new == 'no':
                break
    return user_dict

def login(user_dict):
    username = input('Please Enter your Username: ').strip()
    password = input('Please Enter your Password: ').strip()
    if username not in user_dict:
        print('Username not found!')
        return False
    elif user_dict[username] == password:
        print('Login Successful!')
        return True
    else:
        print('username or password may not correct!')
        return False

user_dict = register()

#装饰器
def auth(f):
    """
    你的装饰器完成， 访问被装饰函数之前，写一个三次登陆认证的功能， 登录成功， 让其访问被装饰的函数，登录没有成功，不让访问。
    """
    def inner(*args, **kwargs):
        """访问函数之前的操作， 功能"""
        if login(user_dict):
            ret = f(*args, **kwargs)
            return ret
        else:
            print('Login Failed.')
    return inner

@auth # article = auth(article)
def article():
    print('Welcome to the article Page!')


def comment():
    print('Welcome to the Comment Page!')

@auth
def dairy():
    print('Welcome to the Dairy Page!')

article()
comment()
dairy()