#!/usr/bin/env python3
import fcntl
from consolemenu import *
from consolemenu.items import *
from filelock import FileLock
import os

from graphics import splash
from colorama import Fore, Style
#from termcolor import colored


users = {}
user = {}
messages = {}
search = {}
logins = []
user['login'] = ''
user['is_auth'] = False
word = "narwhal"


def load_users():
    global users
    with open("./users.txt") as r:
        users = {x[0]: {'login': x[0], 'password': x[1], 'word': x[2]} for x in map(lambda x: x.split(':'), filter(lambda x: x, r.read().split('\n')))}


def load_logins():
    global logins
    with open("./users.txt") as r:
        logins = []
        logins_file = [x[0] for x in map(lambda x: x.split(':'), filter(lambda x: x, r.read().split('\n')))]
        for i in logins_file:
            if i not in logins:
                logins.append(i)


def check_auth():
    global users
    load_users()
    if user['is_auth'] == False:
        print(Fore.RED + 'Sign in please!' + Style.RESET_ALL)
        print(Fore.GREEN)
        input()
        main_menu()


def save_users():
    global users
    with open("./users.txt", "w") as w:
            fcntl.flock(w, fcntl.LOCK_EX)
            for x in users:
                w.write("{}:{}:{}\n".format(users[x]['login'], users[x]['password'], users[x]['word']))
            fcntl.flock(w, fcntl.LOCK_UN)


def auth_menu():
    def register():
        global users
        print("Registration")
        login = input("Enter Login: ")
        if login in users:
            print(Fore.RED + "Already registred!" + Style.RESET_ALL)
            print(Fore.GREEN)
            input()
            return

        password = input("Enter Password: ")
        with open("./users.txt", "a") as w:
            fcntl.flock(w, fcntl.LOCK_EX)
            w.write("{}:{}:{}\n".format(login, password, word))
            fcntl.flock(w, fcntl.LOCK_UN)
            load_users()
            print("Created user {} with password {}.\nPress any key.".format(login, '*' * len(password)))
            input()

    def recovery():
        global users
        print("Forgot your password?\n")
        login = input("Your login: ")
        load_users()

        if login in users:
            word = input("Give me magic word: ")
            if word == users[login]['word']:
                password = input("New Password: ")
                users[login]['password'] = password
                save_users()
            else:
                print(Fore.RED + "Bad word" + Style.RESET_ALL)
                print(Fore.GREEN)
                input()
        else:
            print(Fore.RED + "I don't know you!" + Style.RESET_ALL)
            print(Fore.GREEN)
            input()

    def auth():
        print("Authorization")
        try:
            login = input("Enter Login: ")
            load_users()
            users[login]['login']
        except:
            print(Fore.RED + "Invalid login" + Style.RESET_ALL)
            print(Fore.GREEN)
            input()
            return

        password = input("Enter Password: ")
        if password != users[login]["password"]:
            print(Fore.RED + "Invalid Password" + Style.RESET_ALL)
            print(Fore.GREEN)
            input()
            return
        print("You magic word is: " + word)
        user['login'] = login
        user['password'] = password
        user['is_auth'] = True
        print("OK. Press any key.")
        input()

    menu = ConsoleMenu("User menu       User: {}".format(user['login']), splash())
    user_reg = FunctionItem("Registration", register)
    user_auth = FunctionItem("Authorization", auth)
    user_rec =  FunctionItem("Recovery", recovery)
    menu.append_item(user_reg)
    menu.append_item(user_auth)
    menu.append_item(user_rec)
    menu.show()


def chat():
    load_users()
    check_auth()

    def new_message():
        User_name = input("User name: ")
        if User_name not in users:
            print(Fore.RED + "Not existing user" + Style.RESET_ALL)
            print(Fore.GREEN)
            input()
            return
        message = input("Enter your message: ")
        with open("messages/"+user['login']+"_"+User_name+".txt", "a") as w:
            fcntl.flock(w, fcntl.LOCK_EX)
            w.write("FROM: {}\nTO: {}\nMESSAGE: {}\n\n".format(user['login'], User_name, message))
            fcntl.flock(w, fcntl.LOCK_UN)
        print("Send message... OK. Press any key")
        input()

    def history():

        def inbox():

            return "clear && cat messages/*_{}.txt | sed '$ a\Press any key to quit.\n' && read var1".format(user['login'])

        def outbox():
            return "clear && cat messages/{}_*.txt | sed '$ a\Press any key to quit.\n' && read var1".format(user['login'])

        def search():
            search_name = input("What you search?\nSearch: ")

            def search_inbox():
                return "clear && egrep -h 'MESSAGE: [a-zA-Z 0-9]{0,}"+search_name+"' messages/*_"+user['login']+".txt | sed '$ a\Press any key to quit.\n' && read var1"

            def search_outbox():
                return "clear && egrep -h 'MESSAGE: [a-zA-Z 0-9]{0,}"+search_name+"' messages/"+user['login']+"_*.txt | sed '$ a\Press any key to quit.\n'  && read var1"


            menu = ConsoleMenu("Search menu     User: {} ".format(user['login']), splash())
            search_inbox = CommandItem("Search incoming messages", search_inbox())
            search_outbox = CommandItem("Search outgoing messages", search_outbox())
            menu.append_item(search_inbox)
            menu.append_item(search_outbox)
            menu.show()

        menu = ConsoleMenu("History         User: {} ".format(user['login']), splash())
        inbox = CommandItem("Incoming messages", inbox())
        outbox = CommandItem("Outgoing messages", outbox())
        search = FunctionItem("Search", search)
        menu.append_item(inbox)
        menu.append_item(outbox)
        menu.append_item(search)
        menu.show()

    def all_users():
        global logins
        load_logins()
        for login in logins:
            print(login)
        input()

    menu = ConsoleMenu("Chat menu       User: {} ".format(user['login']), splash())
    new_message = FunctionItem("New message", new_message)
    history = FunctionItem("History", history)
    all_users = FunctionItem("List of users", all_users)
    menu.append_item(new_message)
    menu.append_item(history)
    menu.append_item(all_users)
    menu.show()


def main_menu():
    print(Fore.GREEN)
    menu = ConsoleMenu("Main menu         User: {}".format(user['login']), splash())
    user_menu_item = FunctionItem("User menu", auth_menu)
    chat_menu_item = FunctionItem("Chat menu", chat)
    menu.append_item(user_menu_item)
    menu.append_item(chat_menu_item)
    load_users()
    menu.show()


if __name__=='__main__':
    main_menu()
