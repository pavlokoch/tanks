import socket
import sys
import time

def connect(address):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# scan local network
	result = sock.connect_ex((address,10000))	
	if result == 0:
		return sock
	else:
		return 0

def send_message(sock,message):	
#	try:
    
#    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)
	
#	    amount_received = 0
#	    amount_expected = len(message)
#	    while amount_received < amount_expected:
#	        data = sock.recv(16)
#	        amount_received += len(data)
#	        print >>sys.stderr, 'received "%s"' % data

def read_buffer(sock):
        return sock.recv(16)
	
def disconnect(sock):
	# send disconnect request to server
	send_message(sock,"disconnect")
	sock.close()
