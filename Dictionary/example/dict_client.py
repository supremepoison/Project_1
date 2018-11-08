#coding=utf-8

from socket import *
import sys 
import getpass
#网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    s= socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return
    
    while True:
        print('''
        ==========Welcome==========
        --1.注册   2.登录    3.退出--
        ===========================
        ''')
        try:

            cmd = int(input('Enter the number>>'))
        except Exception as e :
            print('Command is incorrect')
            continue
        
        except KeyboardInterrupt:
            sys.exit('Thank you')

        if cmd not in [1,2,3]:
            print('Does not have this option')
            continue
        
        elif cmd == 1:
            do_register(s)

        elif cmd ==2:
            do_login(s)
        else:    
            s.send(b'E')
            sys.exit('Thank you ')

def do_register(s):
    while True:
        name = input('Name:')
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Again:')

        if (' 'in name ) or (' 'in passwd):
            print('用户名或者密码不能有空格')
            continue
        
        if passwd != passwd1:
            print('两次密码不一致')
            continue
        
        msg = 'R %s %s' % (name,passwd)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(1024).decode()
        if data == 'OK':
            print('注册成功')
        elif data == 'EXISTS':
            print('该用户已存在')
        else:
            print('注册失败')
        return

def do_login(s):
    while True:
        name = input('User:')
        passwd = getpass.getpass()
        
        msg = 'L %s %s' % (name,passwd)
       
        s.send(msg.encode())
        
        data = s.recv(1024).decode()
        if data == 'OK':
            print('登录成功')
            login(s,name)
           
        else:
            print('登录失败')
           
        return

def login(s,name):
      while True:
        print('''
        ============Welcome===========
        --1.查词   2.历史记录    3.注销--
        ==============================
        ''')
        try:

            cmd = int(input('Enter the number>>'))
        except Exception as e :
            print('Command is incorrect')
            continue
        
        except KeyboardInterrupt:
            sys.exit('Thank you')

        if cmd not in [1,2,3]:
            print('Does not have this option')
            continue
        
        elif cmd == 1:
            do_query(s,name)

        elif cmd ==2:
            do_history(s,name)
        else:    
            return
def do_history(s,name):
    msg = 'H %s' % name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            print(data)
            if data == '##':
                break
    else:
        print('There is no history')



def do_query(s,name):
    while True:
        word = input('Word:')
        if word == '##':
            break

        msg = 'Q %s %s' %(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()

        if data == 'FAILED':
            print('Does not match any words')

        else:
            print(data)

if __name__ == '__main__':
    main()