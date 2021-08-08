#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: olinjohnson

"""

import socket
import threading

host = '127.0.0.1'
port = 7622

class client(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    def run(self):
        while True:
            data = self.conn.recv(1024)

            if not data:
                print(addr, ' DISCONNECTED')
                break

            print(addr, ': ', data.decode('utf-8'))
    
            conn.sendall(data)

        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.bind((host, port))
    sock.listen()

    while True:
        (conn, addr) = sock.accept()

        print('Connection from: ' , addr)

        t = client(conn, addr)
        
        t.start()