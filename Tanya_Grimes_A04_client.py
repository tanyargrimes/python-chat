# !/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
Chat Client

Created on Fri Jul 10 09:18:54 2020

@authors: Tanya Grimes
    
Code modified from:
-    https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
-    https://realpython.com/python-gui-tkinter/
-    http://effbot.org/zone/tkinter-scrollbar-patterns.htm#:~:text=to%20standard%20widgets.-,The%20Scrollbar%20Interface,the%20Text%20widget.
'''


#------------------------------------------
# Library Imports

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk


#------------------------------------------
# Function Definitions

def validate_ipv4(address):
    ''' validates host input and prints message if invalid '''
    
    is_valid = True
    
    if address == '' or address == '0.0.0.0':
        print('IP address format is not valid for the client setup.')
        is_valid = False
    elif (len(address) > 0 and address.count('.') != 3):
        # a valid ipv4 address should contain 3 dots
        print('IP address is not valid.')
        print('The format should contain 3 dots for wiFi. E.g. 158.12.0.13')
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
        
        # returns true if no errors were found in the looping conditions
        return is_valid
    
    else:
        return True
    
    # returns true if no errors were found
    return is_valid


def retrieve_address(type):
    ''' recursively validates the input and only returns when valid '''
    
    host_input = input('Please enter the ' + type + ' IP address: ').strip()
        
    if validate_ipv4(host_input):
        return host_input
    else:
        return retrieve_address(type)
 

def validate_port(port, s_port, type):
    ''' validates port input and prints message if invalid '''
    
    if port == '':
        print('Port number is required.')
    elif not port.isnumeric():
        print('Port number is not valid.')
        print('Only numbers are allowed.')
    elif not(int(port) > 0 and int(port) < 65536):
        print('Port number is not valid.')
        print('Number should be between 1 and 65535 inclusive.')
    elif s_port != None and int(port) == s_port and type.lower() == 'client':
        print('Port number is not valid.')
        print('The Client cannot share the same port as the Server.')
    else:
        return True
    
    # return false if errors were found
    return False
        
 
def retrieve_port(type, s_port = None):
    ''' recursively validates the input and only returns when valid '''
    
    port_input = input('Please enter the ' + type + ' port number: ').strip()
    
    # check conditions for a valid port number
    if validate_port(port_input, s_port, type):
        return int(port_input)
    else:
        return retrieve_port(type, s_port)
    

def receive_message():
    ''' Handles receipt of message '''
    
    while True:
        try:
            receiving_msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            
            # adds message to chat list box
            lst_messages.insert(tk.END, receiving_msg)
            lst_messages.insert(tk.END, '')
            
            # sets the vertical view to see the end of the list
            lst_messages.yview(tk.END)
            
        except OSError:  
            # Possibly client has left the chat.
            break


def send_message(event = None):
    ''' Displays the current message and sends to the server '''
    
    # stores the current input text
    msg_raw = msg_current.get()
    
    # clears the input box for re-use
    msg_current.set('')
    
    # sends the message to the server
    client_socket.send(bytes(msg_raw, 'utf8'))
    
    # allows user to type when to close the widget
    if msg_raw == '{x}':
        client_socket.close()
        gui_client.destroy()


def on_closing(event = None):
    ''' Prepares for the closing the widget closing 
    by passing appropriate exit messages '''
    
    msg_current.set('{x}')
    send_message()


#------------------------------------------
# Tkinter GUI Definitions

TK_THEME_COL = 'green'
TK_BTN_TXT_COL = 'white'
TK_FRM_BG_COL = '#eee'

gui_client = tk.Tk()
gui_client.title('Chatter Box')

lbl_greeting = tk.Label(
    text = 'Welcome to Chatter Box!'.upper(),
    fg = TK_THEME_COL,
    width = 70,
)
lbl_greeting.pack()

# adds frame to hold the list box and scrollbar
frm_messages = tk.Frame(
    master = gui_client,
    relief = tk.FLAT,
    borderwidth = 5
)

# allows the frame to grow as the widget expands
frm_messages.pack(
    fill = tk.BOTH,
    expand = True
)

# scrolls the frame to see previous messages
srl_scrollbar = tk.Scrollbar(
    master = frm_messages
)

# adds message list to frame and activates scrollbar
lst_messages = tk.Listbox(
    master = frm_messages,
    height = 20,
    bg = TK_FRM_BG_COL,
    yscrollcommand = srl_scrollbar.set
)
lst_messages.pack(
    side = tk.LEFT,
    fill = tk.BOTH,
    expand = True
)

# adds extra config to scrollbar after listbox is defined and loaded
srl_scrollbar.config(command = lst_messages.yview)
srl_scrollbar.pack(
    side = tk.RIGHT,
    fill = tk.Y
)

# stores input as a string variable
msg_current = tk.StringVar()

# adds the input box
input_box = tk.Entry(
    width = 80,
    textvariable = msg_current
)
# binds return key to input with send_message call when pressed
input_box.bind("<Return>", send_message)
input_box.pack(
    side = tk.LEFT,
    fill = tk.BOTH,
    expand = True
)

# adds send button with send_message call on button click
btn_send = tk.Button(
    text = 'Send',
    width = 9,
    height = 2,
    bg = TK_THEME_COL,
    fg = TK_BTN_TXT_COL,
    command = send_message
)
btn_send.pack(
    side = tk.RIGHT
)

# calls to the on_closing function when the widget X button is clicked
# this seems to work on Windows 10, but will display forcibly closed connection
# message on the server console.
gui_client.protocol('WM_DELETE_WINDOW', on_closing)


#--------------------------------------------------------------
# Variable / Constant Definitions & Client to Server Connection

print('\n-------------------------------------------------------')
print('* Python Socket Chat - Client Setup\n')
print('* This application has been set up to allow the')
print('  server and client(s) to communicate once they')
print('  are all on the same LAN WiFi network.\n')
print('* It is limited to one client per machine.\n')
print('* The server must be run first.\n')
print('* The server IP address and port number are required.')
print('  For convenience this information is displayed')
print('  after the server has started successfully')
print('  and can be used to fill the prompts here.\n')
print('* There is no custom check for the correct server WiFi IP address,')
print('  so a built-in error message will not be seen until all')
print('  prompts have been filled in successfully.\n')
print('* It is the same for a correct client WiFi IP address.\n')
print('* If a built-in error is thrown, please open a new Python console')
print('  and close the previous one to kill any lingering connections.\n')
print('* If the server address was left empty or has the format:')
print('  0.0.0.0 on the server setup, the server address to be entered')
print('  on the client setup must be the actual LAN WiFi IP address.\n')
print('* Empty string and 0.0.0.0 server formats were allowed for quick')
print('  testing between a client and server on the same machine only.\n')
print('* The client IP address and port number are also required')
print('  to verify the client is on the same LAN WiFi network,')
print('  especially if it is not on the same machine as the server.\n')
print('* It is assumed IPv4 addresses will be used.\n')
print('* It is assumed only one server will be running.\n')
print('* It is assumed all ports entered are available.')
print('-------------------------------------------------------\n')

S_HOST = retrieve_address('Server')
S_PORT = retrieve_port('Server')
C_HOST = retrieve_address('Client')
C_PORT = retrieve_port('Client', S_PORT)
S_ADDRESS = (S_HOST, S_PORT)
C_ADDRESS = (C_HOST, C_PORT)
BUFFER_SIZE = 1024
print('\nServer Address:', S_ADDRESS)
print('Client Address:', C_ADDRESS)

client_socket = socket(AF_INET, SOCK_STREAM)

# need to bind client address to verify client on a different machine is on
# the same LAN WiFi network as the server
client_socket.bind(C_ADDRESS)
client_socket.connect(S_ADDRESS)

receive_thread = Thread(target = receive_message)
receive_thread.start()

# opens chat widget and listens for events to prevent another window from opening
gui_client.mainloop()


