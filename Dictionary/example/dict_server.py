'''
name:superman
moudles:pymsql
This is a dict project from AID
'''


from socket import *
import pymysql
import os
import sys
from threading import Thread
import time

#定义需要的全局变量
DICT_TEXT = '/home/tarena/AID1808/Project_1/Dictionary/example/dict.txt'
HOST = '0.0.0.0'
PORT = 4567
ADDR = (HOST,PORT)

#处理僵尸进程
def zombie():
        os.wait()


#网络搭建
def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dictionary')

    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(25)

    while True:
        try:
            c,addr = s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
                print(e)
                continue
        #创建子进程
        pid = os.fork()
        if pid == 0:

            s.close()
            do_child(c,db) #子进程函数

        else:
            t = Thread(target = zombie)
            t.setDaemon(True)
            t.start()
            c.close()
            continue

def do_child(c,db):
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit('88')
        elif data[0] == 'R':
            do_register(c,db,data)

        elif data[0] == 'L':
            do_login(c,db,data)
        
        elif data[0] == 'Q':
            do_query(c,db,data)
        
        elif data[0] == 'H':
            do_history(c,db,data)

def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = 'select * from user where name = "%s"' % name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        c.send(b'EXISTS')
        return
    
    #插入用户
    sql = 'insert into user(name,password) values("%s","%s")' % (name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except:
        db.rollback
        s.send(b'Failed')

def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name = '%s' and password = '%s'" %(name,passwd)

    #查找用于
    cursor.execute(sql)
    r = cursor.fetchone()

    if r == None:
        c.send(b'FAILED')
    else:
        c.send(b'OK')

def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
   
        sql = 'insert into history (name,word,time) values("%s","%s","%s")' %(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
       
    
        


    #使用单词本查找
    try:
        f = open(DICT_TEXT)
    except:
        c.send(b'FAILED')
        return

    for line in f:
        tmp = line.split(' ')[0]

        if tmp > word:
            c.send(b'FAILED')
            f.close()
            return

        elif tmp == word:
            c.send(line.encode())
            f.close()
            insert_history()
            
            return

    c.send(b'FAILED')
    f.close()

def do_history(c,db,data):
    l = data.split(' ')
    name = l[1]

    cursor = db.cursor()
    sql = 'select * from history where name = "%s"' % name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b'FAILED')
        return
    else:
        c.send(b'OK')
        time.sleep(0.0000000001)
    for i in r:
        msg = '%s %s %s'%(i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.0000000001)

    c.send(b'##')

    

     

if __name__ == '__main__':
    main()
