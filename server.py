import subprocess
import socket
import sys
import time

def create_server(address):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Bind the socket to the address given on the command line
	server_name = address
	server_address = (server_name, 10000)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(server_address)
	sock.listen(1)
	return sock

def wait_connection(sock):
	connected = False
	while not connected:
	    print >>sys.stderr, 'waiting for a connection'
	    connection, client_address = sock.accept()
	    connected = True
	    try:
	        print >>sys.stderr, 'client connected:', client_address
#	        while True:
#	            data = connection.recv(16)
#	            print >>sys.stderr, 'received "%s"' % data
#	            if data:
#	                #connection.sendall('hi')
#			if data == 'disconnect':
#				print >>sys.stderr, 'closing connection'
#				connection.close()
#				break
#	            else:
#	                break
	    except Exception as e:
	        pass
#	time.sleep(0.5)
	return connection

def read_buffer(connection):
	return connection.recv(16)

def send_message(connection, message):
	connection.sendall(message)		

def kill_server(connection):
	connection.close()
