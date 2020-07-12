# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:18:54 2020

@authors: 
    Gurjap Singh
    Jaibir Singh
    Tanya Grimes
    
Code modified from:
-    https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
-    https://realpython.com/python-gui-tkinter/
-    http://effbot.org/zone/tkinter-scrollbar-patterns.htm#:~:text=to%20standard%20widgets.-,The%20Scrollbar%20Interface,the%20Text%20widget.
"""


#------------------------------------------
# Library Imports

from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread
import tkinter as tk


#------------------------------------------
# Constant Definitions

# will be an input once more
#SHOST = '192.168.0.15'
#SHOST = '172.18.64.129' # Ethernet IP for server
SHOST = '192.168.0.11' #Wifi IP for server
#SHOST = '72.137.51.162' # Public IP
#SHOST = '0.0.0.0'
SPORT = 33000
#CHOST = gethostname()
CHOST = '192.168.0.11' # Wifi IP for client
#CHOST = '172.18.64.129' # Ethernet for client
CPORT = 12348
BUFSIZ = 1024
SADDR = (SHOST, SPORT)
CADDR = (CHOST, CPORT)
print('Address:', SADDR, CADDR)


#------------------------------------------
# Function Definitions

def receive():
    """ Handles receiving of messages """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            if msg[0:2] == 'c-':
                lbl_connum.set('Active: ' + msg[2:])
            else:
                # add messages to end of the list
                lst_messages.insert(tk.END, msg)
                lst_messages.insert(tk.END, '')
                
                # set the vertical view to see the end of the list
                lst_messages.yview(tk.END)
            
        except OSError:  
            # Possibly client has left the chat.
            break


def send(event = None):
    """ Displays the current message and sends to server """
    
    # stores the current input text
    msg_raw = msg_current.get()
    
    print(msg_raw)
    
    # clears the input box for re-use
    msg_current.set('')
    
    # sends the message to the server
    client_socket.send(bytes(msg_raw, 'utf8'))
    
    # allows user to type when to close the widget
    if msg_raw == '{x}':
        client_socket.close()
        gui_client.destroy()


def on_closing(event = None):
    """ Executes on closing of the widget """
    msg_current.set('{x}')
    send()


#------------------------------------------
# Tkinter GUI Definitions

gui_client = tk.Tk()
gui_client.title("Chatter Box")

frm_title = tk.Frame(
    master = gui_client,
    relief = tk.FLAT
)
frm_title.pack(
    fill = tk.BOTH,
    #expand = True
)

lbl_greeting = tk.Label(
    master = frm_title,
    text = 'Welcome to Chatter Box!'.upper(),
    #width = 60,
    fg = 'green',
    #bg='grey',
)
lbl_greeting.pack(
    side = tk.LEFT,
    fill = tk.BOTH,
    anchor = tk.W,
    expand = True
)

# stores label text as a string variable
lbl_connum = tk.StringVar()

lbl_connections = tk.Label(
     master = frm_title,
    text = '',
    width = 10,
    fg = 'green',
    #bg='purple',
    padx = 30,
    textvariable = lbl_connum
)
lbl_connections.pack(
    side = tk.RIGHT,
    fill = tk.Y,
    anchor = tk.E,
    expand = True
)

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
    yscrollcommand = srl_scrollbar.set
)
lst_messages.pack(
    side = tk.LEFT,
    fill = tk.BOTH,
    expand = True
)

# add extra config after listbox is defined and load
srl_scrollbar.config(command = lst_messages.yview)
srl_scrollbar.pack(
    side = tk.RIGHT,
    fill = tk.Y
)

# stores input as a string variable
msg_current = tk.StringVar()

# add the input box
input_box = tk.Entry(
    width = 80,
    textvariable = msg_current
)
input_box.bind("<Return>", send)
input_box.pack(
    side = tk.LEFT,
    fill = tk.BOTH,
    expand = True
)

# add send button
btn_send = tk.Button(
    text='Send',
    width = 7,
    height = 2,
    bg = 'green',
    fg = 'white',
    command = send
)
btn_send.pack(
    side = tk.RIGHT
)

# calls to on_closing function when the widget X button is clicked
gui_client.protocol("WM_DELETE_WINDOW", on_closing)


#------------------------------------------
# Open Client Widget

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.bind(CADDR)
client_socket.connect(SADDR)

receive_thread = Thread(target = receive)
receive_thread.start()

# listens for events to prevent another window from opening
gui_client.mainloop()


