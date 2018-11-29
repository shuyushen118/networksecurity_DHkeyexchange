from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64decode
from Crypto.Hash import HMAC
import hashlib
import base64
import hmac
import socket
import sys
import select
import argparse
import signal
import random

SOCKET_LIST = [];


def handler(signum,frame):
    """ handle a SIGINT (ctrl-C) keypress """
    for s in SOCKET_LIST:                 #close all sockets
        s.close()
    sys.exit(0)

#server program
def s():
    HOST =''
    PORT = 9999
    #create an INET, STREAMing socket
    listen_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #set to reuse address
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind socket to an address
    listen_socket.bind((HOST, PORT))
    #listen for connections made to socket, 10 is the maxium que connection
    listen_socket.listen(10)
    #empty socket
    client_socket = []
    #infinite loop for reciving signal
    not_key_exchanged = True
    if True:
        #list store keyboardinput and established connection
        inputs = [sys.stdin,listen_socket]+client_socket
        #using select to store data and not blocking communication
        read_list, write_list, error = select.select(inputs,[],[])
        for r in read_list:
            #a new connection established
            if r is listen_socket:
                conn,addr = r.accept()
                #add new connection to the client socket list
                client_socket.append(conn)
#                print " in the key exchanged "
                #store the A reicved from client
                A_recived = conn.recv(1024)
                sys.stdout.flush()
#                print (A_recived)
#                print("********************")
                #generate B
                p = 0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc688c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b #p
                g = 2
                b = random.randrange(1,p)
                B = pow (g,b,p)
#                print (B)
                #send B to client
                conn.send(str(B) + '\n')
                sys.stdout.flush()
                #compute K
                A = int(A_recived)
                K = pow(A,b,p)
#                print"**********"
                print K


#client program
def c():
    not_send_1 = True;
    ##    print ("in the client")
    HOST =''
    PORT =9999
    #create an INET, STREAMing socket
    connect_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connect_socket.connect((HOST,PORT))
    if True:
        #generate privare key and send A
#        A = genPublickey()
        p = 0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc688c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b #p
        g = 2
        a = random.randrange(1,p)
#        print "random number is "
#        print a
#        print "***********"
        A = pow (g,a,p)
        #send A to the sever
        connect_socket.send(str(A) + '\n')
        sys.stdout.flush()
        #recive B from server
        B = connect_socket.recv(1024)
#        print B;
        #change B to an integer
        B = int(B)
        sys.stdout.flush()
        #compute K
        K = pow(B,a,p)
#        print "************"
        print K




argv_1 = sys.argv[1]
signal.signal(signal.SIGINT,handler)

if argv_1 == "--s":
    s()
elif argv_1 == "--c":
    c()
for sock in SOCKET_LIST:
    sock.close();
sys.exit(0);
return 0;
