# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:15:30 2020

@authors: 
    Gurjap Singh
    Jaibir Singh
    Tanya Grimes

Code modified from:
    https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
"""



#------------------------------------------
# Library Imports

from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread
import datetime as dt


#------------------------------------------
# Function Definitions

def accept_incoming_connections():
    """ Sets up handling for incoming clients. """
    while True:
        client, client_address = SERVER.accept()
        #print("%s:%s has connected." % client_address)
        client.send(bytes('Enter your name to join the chat.', 'utf8'))
        addresses[client] = client_address
        Thread(target = handle_client, args = (client,client_address)).start()


def handle_client(client, client_address):
    """ Handles a single client connection. """
    client_name = client_address[0]
    user_name = (client.recv(BUFSIZ).decode("utf8")).strip()
    #print('name on start',user_name)
    # provide a default name if the name is empty
    if len(user_name) == 0:
        user_name = 'Anonymous'
    
    # set name to uppercase
    #user_name = user_name.upper()
    
    welcome = 'Welcome %s! If you ever want to quit, type {x} to exit.' % user_name
    
    # sends to newly joined client only
    client.send(bytes(welcome, "utf8"))
    print(welcome)
    
    # adds new client by name to keeps track of all active clients
    clients[client] = user_name
    
    print('clients', clients)
    msg = '{0} has just been connected. Total connections is {1}.'.format(client_name, len(clients))
    
    broadcast(bytes(msg, 'utf8'))
    
    #print('wait...')
    
    # update active connections display
    #broadcast(bytes('c-' + str(len(clients)), 'utf8'))

    while True:
        msg = client.recv(BUFSIZ)
        
        #print('msg - server', msg)
        if msg != bytes("{x}", "utf8"):
            # set prefix to include date and time
            dte_now = (dt.datetime.now()).strftime('%Y-%m-%d %H:%M')
            prefix = '[ ' + str(dte_now) + ' ]     ' + user_name + ':  '
            broadcast(msg, prefix)
        else:
            # deletes exiting client to keeps track of all active clients accurately
            del clients[client]
            #print('clients length on close',len(clients))
            # update active connections display
            #broadcast(bytes('c-' + str(len(clients)), 'utf8'))
            client.send(bytes("{x}", "utf8"))
            client.close()
            
            broadcast(bytes("%s has left the chat." % user_name, "utf8"))
            
            msg = '{0} has disconnected. Total connections is {1}.'.format(client_name, len(clients))
            broadcast(bytes(msg, 'utf8'))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        # included condition to prevent certain messages from being displayed
        # to the newly joined client
        # if exclude_new and client == sock:
        #     pass
        # else:
        sock.send(bytes(prefix, "utf8") + msg)


#------------------------------------------
# Constant & Variable Definitions
        
clients = {}
addresses = {}
#HOST = '0.0.0.0'
#HOST = '' # accepts connections on all available IPv4 connections
#HOST = '72.137.51.162' # Public IP
HOST = '192.168.0.11' # Wifi IP
#HOST = gethostbyname(gethostname()) # Ethernet IP - only works for local clients
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
print('Address:', ADDR)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target = accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()