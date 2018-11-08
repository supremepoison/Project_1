'''
电子词典客户端
'''
from socket import *
import sys 


class Client():
    def __init__(self,sockfd):
        self.sockfd = sockfd
        
    def first_level(self):
        while True:
            print('--------Dictionary---------')
            print('***                  ***')
            print('***      Login        ***')
            print('***      Regidter     ***')
            print('***      Quit        ***')
            print('***------------------***')
            print()
            
            choice = input('Choice(small letter):')
            if choice == 'login':
                self.login()
            elif choice == 'register':
                self.register()
            elif choice == 'quit':
                self.quit()
            else:
                print('Enter the right command')
                continue

    def register(self):
        name = input('Name:')
        pwd = input('Password:')
        data = 'R '+name+'~'+pwd
        self.sockfd.send(data.encode())

        receive = self.sockfd.recv(1024).decode()
        if receive == 'O':
            print('This name already exits')
            return self.first_level()
        elif receive == 'Y':
            print('Register successfully!')
            return self.first_level()
    
    def login(self):
        name = input('Name:')
        pwd = input('Password:')
        data = 'L '+name+'~'+pwd
        self.sockfd.send(data.encode())
        receive = self.sockfd.recv(1024).decode()
        if receive == 'N':
            print('This user does not exist')
            return self.first_level()
        elif receive == 'T':
            print('Welcome')
            return self.second_level()
        elif receive == 'F':
            print('The password is not correct')
            return self.first_level()

    def quit(self):
        data = 'Q '
        self.sockfd.send(data.encode())
        receive = self.sockfd.recv(1024).decode()
        if receive == 'EXIT':
            sys.exit('88')
        


    def second_level(self):
        while True:
            print('--------Dictionary---------')
            print('***                  ***')
            print('***      Search        ***')
            print('***      History     ***')
            print('***      Logout        ***')
            print('***------------------***')
            print()

            choice = input('Choice(small letter):')
            if choice == 'search':
                self.search()
            elif choice == 'history':
                self.history()
            elif choice == 'logout':
                self.logout()
            else:
                print('Enter the right command')
                continue
            
    def search(self):
        word = input('Enter the word:')
        data = 'S '+word
        self.sockfd.send(data.encode())
        receive= self.sockfd.recv(256).decode()

        if receive == 'N':
            print('This word does not exists')
            
        else:
            print(word,':',receive)

    def history(self):
        pass

    def logout(self):
        print('See ya~')
        self.first_level()

            

        # if receive  == 'Y':
        #     password =input('Password:')
        # elif receive == 'O':
        #     print('This name is already exists')
        #     return self.first_level()
        





if __name__ == '__main__':

    server_host = '127.0.0.1'
    server_port = 5678
    server_addr = (server_host,server_port)
    sockfd = socket()
    sockfd.connect(server_addr)

    client = Client(sockfd)
    client.first_level()
    