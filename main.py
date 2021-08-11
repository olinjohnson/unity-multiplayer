#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: olinjohnson

"""

import socket
import threading
import json

host = '127.0.0.1'
port = 7622

players = []

class Client(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
    def run(self):
        
        # Get initial name of player who connects
        # Add connecting  player to players[] array
        n = self.conn.recv(128)
        print(n.decode('ASCII'))
        
        id = len(players)
        new_player = {
            'username': n.decode('ASCII'),
            'position': [0, 0, 0],
        }
        players.append(new_player)
        
        # Listen for data from the player
        while True:
            
            # Get posititional data from player
            data = self.conn.recv(1024)
            
            # Check to make sure the player hasn't disconnected
            if not data:
                print(addr, ' ', n, ' DISCONNECTED')
                players.pop(id)
                break

            # Update player's position in players[] array
            parsed_data = json.loads(data)
            players[id]['position'][0] = parsed_data['position'][0]
            players[id]['position'][1] = parsed_data['position'][1]
            players[id]['position'][2] = parsed_data['position'][2]
            
            # Send back positions of other players
            packet = []
            
            for i in players:
                packet.append(i)
            
            packet.pop(id)
            serialized_packet = json.dumps(packet)
            print(serialized_packet, n)
            
            conn.send(serialized_packet.encode('ASCII'))

        conn.close()


# Start socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.bind((host, port))
    sock.listen() 

    # Listen for connections
    while True:
        
        # On each connection, send client to a new thread
        
        (conn, addr) = sock.accept()

        print('Connection from: ' , addr)

        th = Client(conn, addr)
        
        th.start()
