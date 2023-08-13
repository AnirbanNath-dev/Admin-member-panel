from time import sleep
import os
import json
import random
from string import ascii_lowercase
from utils.secrets import USERNAME , PASSWORD

MEMBER_DATA = 'data/members/member.json'


def read_data(filepath):
    try:
        with open(filepath , 'r') as f:
            data = json.load(f)
            return data
    except:
        return {}
        
def append_data( data , filepath):
    with open(filepath , 'w') as f:
        json.dump(data , f , indent=4)

def data_env():
    with open('.env', 'r') as f:
        return f.read()

def change_env(data):
    with open('.env', 'w') as f:
        f.write(data)

def tempdata():
    try:
        with open('data/temp/temp_data.json', 'r') as f:
            return json.load(f)
    except:
        return {}

# Admin panel

class Admin():
    def __init__(self):
        self.tempdata = tempdata()
        self.member_data = read_data(MEMBER_DATA)
    
    def show_all_data(self):
        for key in self.member_data:
            print(f"\n{key} : \n\tpassword : {self.member_data[key]['password']}\n\tid : {self.member_data[key]['id']}")
        
        input('\nPress enter to continue: ')


    def delete_all_data(self):
        sure = input('\nAre you sure to delete all data , it can lead to serious issues (Y/N)? : ')

        if sure.upper()=='Y':
            print('Processing..... ')
            sleep(1)
            stored_data = read_data(MEMBER_DATA)
            data = read_data(MEMBER_DATA)
            data.clear()
            append_data(data , MEMBER_DATA)
            print('Data cleared ! You can bring back the data cleared , it will get deleted later .')
            sleep(1)
            again_sure = input('Do you want to recover (Y/N)? : ')
            if again_sure.upper()=='Y':
                print('Processing..... ')
                sleep(1)
                append_data(stored_data , MEMBER_DATA)
                print('Succesfully recovered')
                sleep(1)
                
            elif again_sure.upper()== 'N':
                print('Alert : Your data can be under threat later ')
                sleep(1)

            else:
                print('Wrong command!')
        elif sure.upper()=='N':
            print('Done ! Datas are secured')
        else:
            print('Wrong command!')
        

        
    def change_username(self):
        name = input('\nEnter the new username : ')
        print('Changing....')
        sleep(1)
        print(f'Previous username : {USERNAME}')
        data = data_env()
        data = f'''NAME={name} 
        PASSWORD = {PASSWORD}'''
        change_env(data)
        print(f'New username : {name}')
        sleep(1)

        json_data = self.tempdata

        with open('data/temp/temp_data.json', 'w') as f:
            json_data['username'] = name
            json.dump(json_data , f , indent=4)

    def change_password(self):
        password = input('\nEnter the new password : ')
        print('Changing....')
        sleep(1)
        print(f'Previous password : {PASSWORD}')
        data = data_env()
        data = f'''NAME={USERNAME}\nPASSWORD = {password}'''
        change_env(data)
        print(f'New password : {password}')
        sleep(1)
        json_data = self.tempdata
        with open('data/temp/temp_data.json', 'w') as f:
            json_data['password'] = password
            json.dump(json_data , f , indent=4)
            


    def screen(self):
        admin_name = input('\n\nEnter the username : ')
        admin_password = input('Enter the password : ')

        if os.path.exists('data/temp/temp_data.json') and (('username' in self.tempdata) or ('password' in self.tempdata)):
            
            if 'username' in self.tempdata:
                username = self.tempdata['username']
            else:
                username = USERNAME
                
            if 'password' in self.tempdata:
                password = self.tempdata['password']
            else:
                password  = PASSWORD

        else:
            username = USERNAME
            password = PASSWORD

        if admin_name == username and admin_password == password:
            
            print('\nYou are now in the admin panel')
            sleep(1)
            while True:
                print('\n\n * Show all data\n * Change the password\n * Change username\n * Delete all data\n * Exit\n') 
                opt = input('Select(1-5): ')
                if opt == '1':
                    self.show_all_data()
                elif opt == '2':
                    self.change_password()
                elif opt == '3':
                    self.change_username()
                elif opt == '4':
                    self.delete_all_data()
                    
                elif opt == '5':
                    print('\nYou are out of admin panel')
                    sleep(1)
                    break
                else:
                    print('Wrong command!')
                    continue

        else:
            print('\nSorry , you are not the Admin of this page !')
            sleep(1)



# Member panel

class New_Member():
    def __init__(self,name):
        self.name = name
        self.getdata = read_data(MEMBER_DATA)
            
    
    def get_unique_id(self):
        id = ''
        for i in range(10):
            id += random.choice(ascii_lowercase)
        
        return id

    def not_a_robot(self):
        while True:
            riddle_list = [random.choice(ascii_lowercase) for _ in range(4)]
            riddle_str = ''.join(riddle_list)

            captcha = input(f'\nNot a robot : Type in alphabetical order ({riddle_str}) : ')
            riddle_list.sort()

            if captcha == ''.join(riddle_list):
                sleep(1)
                print('Verification done !')
                break

            else: 
                sleep(1)
                print('Falied , Try again !')
                continue


    def details(self):
        self.password = input('\nCreate a new password : ')
        while True:
            verify_password = input('Confirm the password : ')
            if verify_password != self.password: 
                print('Incorrect password')
                continue
            else:
                print('Your password has been set !')
                break
        unique_id = self.get_unique_id()
        self.not_a_robot()
        sleep(1)
        print(f'\nYour id : {unique_id}')
        sleep(1)
        data = {
                "password" : self.password,
                "id" : unique_id
            }
        
        self.getdata[self.name] = data
        append_data(self.getdata , MEMBER_DATA)



        
        
    def screen(self):
        self.details()

#Login 

class Login():
    def __init__(self, name):
        self.name =  name
        self.getdata = read_data(MEMBER_DATA)

    def getdetails(self):


        if self.name not in self.getdata:
            print('\nYou are not a valid member')
            sleep(1)

        else:
            password = input('\nEnter the password : ')
            id = input('Enter your id : ')
            if password != self.getdata[self.name]['password'] and id != self.getdata[self.name]['id']:
                
                sleep(1)
                print('Wrong password or id !')
                sleep(1)
            else:
                sleep(1)
                print('\nSuccesfully logged in ')
                sleep(1)


    def screen(self):
        self.getdetails()

def main():
    
    print('\n\n\t\t+--------------------+')
    print('\t\t|  \033[1mWelcome to ANBIT\033[0m  |')
    print('\t\t+--------------------+')

    sleep(1)
    while True:
        print('\n * Admin page\n * Sign\n * Login\n * Exit')
        opt = input('Select (1-4) : ')
        if opt == '1':

            admin = Admin()
            admin.screen()
            
        elif opt == '2':
            name = input('\n\nEnter your name: ')
            member = New_Member(name)
            member.screen()
            
        elif opt == '3':
            name = input('\n\nEnter your name : ')
            login_member = Login(name)
            login_member.screen()
        
        elif opt == '4':
            if os.path.exists('data/temp/temp_data.json'):
                os.remove('data/temp/temp_data.json')
            print('Thanks for using !')
            break
        else:
            if os.path.exists('data/temp/temp_data.json'):
                os.remove('data/temp/temp_data.json')
            print('Wrong command!')
            break



    


if __name__ == '__main__':
    main()
    
