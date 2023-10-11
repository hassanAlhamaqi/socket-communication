import os
import argparse
import threading

from posixpath import split
from time import sleep

from os import error, path as os_path

file_path = os_path.dirname(os_path.realpath(__file__))

parser = argparse.ArgumentParser(description='DDS Chat Application')

parser.add_argument('user', help='User name', type=str)
parser.add_argument('group', help='Group name', type=str)
parser.add_argument('-f', '--firstname', help='First name', type=str, default='')
parser.add_argument('-l', '--lastname', help='Last name', type=str, default='')

args = parser.parse_args()

###

import rticonnextdds_connector as rti

lock = threading.RLock()
finish_thread = False

def user_subscriber_task(user_input):
    global finish_thread

    while finish_thread == False:
        try:
            user_input.wait(500)
        except rti.TimeoutError as error:
            continue

###

def message_subscriber_task(message_input):
    global finish_thread

    while finish_thread == False:
        try:
            message_input.wait(500)
        except rti.TimeoutError as error:
            continue

###

#def command_task(user, message_output, user_input):
def command_task(user_input):
    global finish_thread

    while finish_thread == False:
        command = input("Enter command: ")
        if command == "exit":
            finish_thread = True
        elif command == "list":
            continue
###
        elif command.startswith("send"):
            continue
###
        else:
            print("Unknown command")


sleep(10)
