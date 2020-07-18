# !/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
PROG8420 - Programming for Big Data

Assignment 04 Server

Created on Fri Jul 10 09:15:30 2020

@authors: 
    Gurjap Singh
    Jaibir Singh
    Tanya Grimes

Code modified from:
    https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
'''


#------------------------------------------
# Library Imports

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime as dt


#------------------------------------------
# Function Definitions

def validate_ipv4(address):
    ''' validates host input and prints message if invalid '''
    
    is_valid = True
    
    if len(address) > 0 and address.count('.') != 3:
        # a valid ipv4 address should contain 3 dots
        print('IP address is not valid.')
        print('The format should contain 3 dots for wiFi. E.g. 158.12.0.13')
        print('or can be empty for local machine testing with one client.')
        is_valid = False
        
    elif len(address) > 0 and address.count('.') == 3:
        # validates values between the dots
        ip_split = address.split('.')
        for i in range(len(ip_split)):
            if ip_split[i] == '':
                print('IP address is not valid.')
                print('Format is missing numbers between dots')
                is_valid = False
                break
            elif not ip_split[i].isnumeric():
                print('IP address is not valid.')
                print('Only numbers are allowed between dots')
                is_valid = False
                break
            elif ip_split[i][0] == '0' and len(ip_split[i]) > 1:
                print('IP address is not valid.')
                print('Please do not use leading 0s')
                is_valid = False
                break
            elif not(int(ip_split[i]) > -1 and int(ip_split[i]) < 256):
                print('IP address is not valid.')
                print('Each number should be between 0 and 255 inclusive')
                is_valid = False
                break
        
        # return true if no errors found in the looping conditions
        return is_valid
    
    else:
        return True
    
    # return false if errors have been found
    return is_valid


def retrieve_address():
    ''' recursively validates the input and only returns when valid '''
    
    host_input = input('Please enter the Server IP address: ').strip()
        
    if validate_ipv4(host_input) == True:
        return host_input
    else:
        return retrieve_address()
 
    
def validate_port(port):
    if port == '':
        print('Port number is required.')
    elif not port.isnumeric():
        print('Port number is not valid.')
        print('Only numbers are allowed.')
    elif not(int(port) > 0 and int(port) < 65536):
        print('Port number is not valid.')
        print('Number should be between 1 and 65535 inclusive.')
    else:
        return True
    
    # return false if errors have been found
    return False


def retrieve_port():
    ''' recursively validates the input and only returns when valid '''
    
    port_input = input('Please enter the Server port number: ').strip()
    
    # check conditions for a valid port number
    if validate_port(port_input):
        return int(port_input)
    else:
        return retrieve_port()
    

def initialize_connection():
    ''' Accepts client connection and prepares client to enter the chat '''
    
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes('Enter your name to join the chat.', 'utf8'))
        
        # keeps track of active client addresses
        addresses[client] = client_address
        
        # open thread to allow client to participate in the chat
        Thread(target = manage_client, args = (client,client_address)).start()


def manage_client(client, client_address):
    ''' Manages a single client connection and any client interactions '''
    
    client_name = client_address[0]
    user_name = (client.recv(BUFFER_SIZE).decode('utf8')).strip()
    
    # provide a default name if the name is empty
    if len(user_name) == 0:
        user_name = 'Anonymous'
    
    # display welcome message with client's user name
    welcome_msg = 'Welcome %s! If you ever want to quit, type {x} to exit.' % user_name
    
    # sends welcome message to new client only
    client.send(bytes(welcome_msg, 'utf8'))
    
    # adds new client by name to keeps track of all active clients
    clients[client] = user_name
    
    # creates connection message with formatting
    connection_msg = '{0} has just been connected. Total connections is {1}.'.format(client_name, len(clients))
    
    # broadcasts connection message to all clients
    broadcast(bytes(connection_msg, 'utf8'))
    
    # keep listening for user input
    while True:
        broadcast_msg = client.recv(BUFFER_SIZE)
        
        # checks if user has entered special characters to exit the chat
        if broadcast_msg != bytes("{x}", "utf8"):
            # sets prefix to include date and time
            dte_now = (dt.datetime.now()).strftime('%Y-%m-%d %H:%M')
            prefix = '[ ' + str(dte_now) + ' ]     ' + user_name + ':  '
            
            # broadcasts message to all clients
            broadcast(broadcast_msg, prefix)
        else:
            # deletes exiting client to keeps track of all active clients accurately
            del clients[client]
            client.close()
            
            # broadcasts to all available clients that a user has left
            user_exit_msg = '%s has left the chat.' % user_name
            broadcast(bytes(user_exit_msg, 'utf8'))
            
            # broadcasts to all available clients that client has disconnected
            disconnection_msg = '{0} has disconnected. Total connections is {1}.'.format(client_name, len(clients))
            broadcast(bytes(disconnection_msg, 'utf8'))
            break


def broadcast(message, prefix=''):
    ''' Broadcasts a message to all clients, with an optional prefix. '''
    for client in clients:
        client.send(bytes(prefix, 'utf8') + message)


#----------------------------------------------------------
# Variable / Constant Definitions and Server Initialization

print('\n--------------------------------------------------')
print('* Python Socket Chat - Server Setup\n')
print('* This application has been set up to allow the')
print('  server and client(s) to communicate once they')
print('  are all on the same LAN WiFi network.\n')
print('* It is limited to one client per machine.\n')
print('* The server must be run first.\n')
print('* If there will only be one client and it sits')
print('  on the same machine as the server, the server')
print('  address can be left empty or entered as: 0.0.0.0\n')
print('* Empty string and 0.0.0.0 formats were allowed for quick')
print('  testing between a client and server on the same machine only.\n')
print('* If there will be at least one client on a')
print('  different machine, please ensure it is connected')
print('  on the same WiFi network as the server and')
print('  use the server LAN WiFi address instead.\n')
print('* There is no custom check for the correct server IP address,')
print('  so a built-in error message will not be seen until all')
print('  prompts have been filled in successfully.\n')
print('* If a built-in error is thrown, please open a new Python console')
print('  and close the previous one to kill any lingering connections.\n')
print('* It is assumed IPv4 addresses will be used.\n')
print('* It is assumed only one server will be running.')
print('--------------------------------------------------\n')


HOST = retrieve_address()
PORT = retrieve_port()
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)
print('\nServer Address:', ADDRESS)

# to store the active clients and addresses
clients = {}
addresses = {}

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target = initialize_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()