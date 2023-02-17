#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket


#HOST = f'10.12.1.1'
PORT = 8787

team = [1,2,3,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22,24]
while True:
    for teamid in team :
        HOST = f'10.12.{teamid}.1'
        print(HOST)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        outdata = 'hello hacker'
        print('send: ' + outdata)
        s.send(outdata.encode())

        indata = s.recv(1024)
        print('recv: ' + indata.decode())

        s.close()               