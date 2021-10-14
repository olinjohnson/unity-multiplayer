#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: olinjohnson

"""

import json

players = {}   

class Player:
    def __init__(self, username):
        self.username = username
        self.position = [0, 0, 0]
        self.rotation = 0.0
        self.animation = [0, 0, 0]

def handle_client(conn, addr):
    
        # Get initial name of player who connects
        # Add connecting  player to players[] array
        pName = conn.recv(128)
        n = pName.decode('ASCII')
        print(n)
        
        new_player = {
            'username': n,
            'position': [0, 0, 0],
            'rotation': 0.0,
            'animation': [0, 0, 0]
        }
        players[n] = new_player
        
        # Listen for data from the player
        while True:
            
            # Get posititional data from player
            data = conn.recv(1024)
            
            # Check to make sure the player hasn't disconnected
            if not data:
                print(addr, ' ', n, ' DISCONNECTED1')
                del players[n]
                break
            
            # Update player's position in players[] array
            parsed_data = json.loads(data)
            players[n]['position'][0] = parsed_data['position'][0]
            players[n]['position'][1] = parsed_data['position'][1]
            players[n]['position'][2] = parsed_data['position'][2]
            players[n]['rotation'] = parsed_data['rotation']
            players[n]['animation'][0] = parsed_data['animation'][0]
            players[n]['animation'][1] = parsed_data['animation'][1]
            players[n]['animation'][2] = parsed_data['animation'][2]
            
            
            
            # Send back positions of other players
            packet = []
            
            for i in players:
                if(i != n):
                    packet.append(players[i])
                    
            serialized_packet = json.dumps(packet)
            
            conn.send(serialized_packet.encode('ASCII'))

        conn.close()
