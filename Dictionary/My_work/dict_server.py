'''
电子词典服务端
'''
from socket import *
from threading import Thread
import pymysql
import sys
class Server():
    def __init__(self,server_addr):
        self.addr = server_addr
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.addr)
        
    def start_server(self):
        self.sockfd.listen(25)
        while True:
            try:

                connfd, addr = self.sockfd.accept()
                print('connect from',addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('server quit')
            except Exception as e:
                print(e)
                continue
            handle_client = Thread(target = self.handle,args =(connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle(self,connfd):
        while True:
            data = connfd.recv(1024).decode()
            # print(data)
            command =data.split(' ')[0]
            detail = data.split(' ')[1]
            if command == 'R':
                self.register(detail,connfd)
            if command == 'L':
                self.login(detail,connfd)
            if command == 'Q':
                self.quit_server(connfd)
            if command == 'S':
                self.search(detail,connfd)

    def database(self):
        self.db = pymysql.connect(host = 'localhost', 
                            user = 'root', 
                            password = '123456', 
                            database = 'dictionary', 
                            charset = 'utf8')

        self.cursor = self.db.cursor()

    def database_close(self):
        self.database()
        self.cursor.close()
        self.db.close()

    def register(self,detail,connfd):
        self.database()
        # print(detail)
        username = detail.split('~')[0]
        pwd = detail.split('~')[1]

        self.cursor.execute('(select name from user where name = "%s");' %username)
        name = self.cursor.fetchall()
        print(len(name) )
        
            
        if len(name)>0 :
             connfd.send('O'.encode())
            
        else:          
            self.cursor.execute('insert into user(name,password) values("%s","%s");'%(username,pwd))
            self.db.commit()
            connfd.send('Y'.encode())
        
            # self.database_close()
    
    def login(self,detail,connfd):
        self.database()
        username = detail.split('~')[0]
        pwd = detail.split('~')[1]
        self.cursor.execute('(select password from user where name = "%s");' %username)
        check = self.cursor.fetchall()

        if len(check) == 0:
            connfd.send(b'N')
        elif pwd == check[0][0]:
            connfd.send(b'T')
        else:
            connfd.send(b'F')

    def quit_server(self,connfd):
        connfd.send(b'EXIT')
     
        connfd.close()
        self.database_close()
        sys.exit('client exit')

    def search(self,detail,connfd):
        self.database()
        # print(detail)
        sql = 'select * from words where word = "%s"' % detail
        try:
            self.cursor.execute(sql)
            check = self.cursor.fetchone()
            print(check[2])
        except:
            self.db.rollback

        if check != None:
            connfd.send(check[2].encode())
        else:
            connfd.send(b'N')





        
        
       





if __name__ == '__main__':
    server_host = '0.0.0.0'
    server_port = 5678
    server_addr = (server_host,server_port)    

    server = Server(server_addr)
    server.start_server()
    