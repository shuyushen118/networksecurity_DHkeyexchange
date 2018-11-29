from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import HMAC
import sys
import socket
import select
import signal
import binascii
import hashlib


SOCKET_LIST = [];

def handler(signum,frame):
    """ handle a SIGINT (ctrl-C) keypress """
    for s in SOCKET_LIST:                 #close all sockets
        s.close()
    sys.exit(0)

def convert_key(key):
    h = SHA256.new(key)
    return h.digest()

def genkey():
    #gnerate 4096 bits key pair
    key = RSA.generate(4096)
    #get the public key
    f = open('mypubkey.pem','w')
    #get public key
    pubkey_pem = key.publickey().exportKey('PEM')
    #store public key
    f.write(pubkey_pem)
    f.close
    #get private key
    f2 = open ('myprikey.pem','w')
    prikey_pem = key.exportKey('PEM')
    f2.write(prikey_pem)
    f2.close

#    f = open('mypubkey.pem','r')
#    key_pub = RSA.importKey(f.read())
#    print key_pub
#    f2 = open('myprikey.pem','r')
#    key_priv =RSA.importKey(f2.read())
#    print"***************"
#    print key_priv
def sign(msg):
    key = RSA.importKey(open('myprikey.pem').read())
    #convert key
    h = SHA256.new(msg)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return signature
    

def verify(signature,):
    key =RSA.importKey(open('mypubkey.pem').read())
    h = SHA.new(msg)
    verifer = PKCS1_v1_5.new(key)
    if verifer.verify(h,signature):
        print "authentic"
    else:
        print "not authentic"


def mypad(somenum):
#    print "in pad"
    return '0'*(4-len(str(somenum)))+ str(somenum)


def c(msg):
    HOST =''
    PORT =9998
    #create an INET, STREAMing socket
    connect_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connect_socket.connect((HOST,PORT))
    if True:
#            #a new connection established and message is comming in
#            #keyboard entered, ready to send message
#            if r is sys.stdin:
        outgoing_message = msg
        #get length of message_
        len_str = len(outgoing_message)
        #pad the length
        len_pad = mypad(len_str)
        len_pad = str(len_pad)
        #hexlfiy the signature
        signature = sign(outgoing_message)
        #hexlify the signature
        signature_hex = binascii.hexlify(signature)
        signature_len = len(signature_hex)
        signature_len = str(signature_len)
        connect_socket.send(len_pad)
        connect_socket.send(outgoing_message)
        connect_socket.send(signature_len)
        connect_socket.send(signature_hex)
#        connect_socket.send(len_pad+outgoing_message+signature_len+signature_hex)
        f = open('data.dat','w')
        f.write(len_pad+outgoing_message+signature_len+signature_hex)
        f.close
        sys.stdout.flush()
def s():
    HOST =''
    PORT = 9998
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
    while True:
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
            #send new message
            #moniter is there any input from the keyboard
            elif r is sys.stdin:
                #message enter from keyboard, sending message
                msg = sys.stdin.readline()
                #encrypt message
                conn.send(msg)
                sys.stdout.flush()
            #no message input then waiting for incoming message from client
            else:
                msg = conn.recv(1024)
                #decrypt message
                if msg =="":
                    break;
                sys.stdout.write(msg)
                sys.stdout.flush()


#main
argv_1 = sys.argv[1]

if argv_1 == "--genkey":
    genkey()
elif argv_1 == "--s":
    s()
elif argv_1 == "--c":
    message = sys.argv[2]
    c(message)
for sock in SOCKET_LIST:
    sock.close();
sys.exit(0);











