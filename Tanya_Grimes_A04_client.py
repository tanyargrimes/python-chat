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

from socket import AF_INET, socket, SOCK_STREAM, gethostname
from threading import Thread
import tkinter as tk


#------------------------------------------
# Constant Definitions

HOST = gethostname()
#HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
print('Address:', ADDR)


#------------------------------------------
# Function Definitions

def receive():
    """ Handles receiving of messages """
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            lst_messages.insert(tk.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event = None):
    """ Displays the current message and sends to server """
    
    # stores the current input text
    msg_raw = msg_current.get()
    
    print(msg_raw)
    
    #lst_messages.insert(msg_raw)
    
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

lbl_greeting = tk.Label(
    text = 'Please follow instructions',
    width = 50,
    fg = 'purple'
)
lbl_greeting.pack()

frm_messages = tk.Frame(
    master = gui_client,
    relief = tk.FLAT,
    borderwidth = 5,
    height = 200,
    bg='#ccc'
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
    width = 70,
    textvariable = msg_current
)
input_box.bind("<Return>", send)
input_box.pack(fill = tk.BOTH)

# add send button
btn_send = tk.Button(
    text='Send',
    width = 10,
    height = 2,
    bg = 'purple',
    fg = 'white',
    command = send
)
btn_send.pack()

# calls to on_closing function when the widget X button is clicked
gui_client.protocol("WM_DELETE_WINDOW", on_closing)


#------------------------------------------
# Open Client Widget

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target = receive)
receive_thread.start()

# listens for events to prevent another window from opening
gui_client.mainloop()


