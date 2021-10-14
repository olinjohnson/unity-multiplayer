#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: olinjohnson

"""

import socket
import _thread
import json

import clientHandler as handler

host = ''
port = 7622

# Start socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.bind((host, port))
    sock.listen() 

    # Listen for connections
    while True:
        
        # On each connection, send client to a new thread
        
        (conn, addr) = sock.accept()

        print('Connection from: ' , addr)

        """
        initialLoginCode = conn.recv(4)
        decodedLoginCode = 
        """
        
        _thread.start_new_thread(handler.handle_client, (conn, addr))