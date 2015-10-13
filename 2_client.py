import sys
import socket
import select
import time
import string

host = 'localhost'
port = 8080
 
def client():
     
    # making TCP/IP socket
	x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # terhubung dengan remote host
	try :
		x.connect((host, port))
	except :
		print 'you was not connected'
		sys.exit()
     
	print 'you was connected to remote host. you can send a messages.'
	sys.stdout.write('## '); sys.stdout.flush()
     
	while True:
		socket_list = [sys.stdin, x]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list, [], [])
		 
		for sock in ready_to_read:      
		
			if sock == x:
				# incoming message from remote server, x
				data = sock.recv(4096)
				if not data :
					print '\nyou was  disconnected from chat server.'
					sys.exit()
				else :
					sys.stdout.write(data)
					sys.stdout.write('## '); sys.stdout.flush()     
			
			else :
				# user memasukkan pesan
				msg = []
				temp = sys.stdin.readline()
				temp1 = string.split(temp[:-1])
				
				d=len(temp1)
				if temp1[0]=="login" :
					
						x.send(temp)
				
				elif temp1[0]=="list" :
					
						x.send(temp)

				elif temp1[0]=="send" :
					
						x.send(temp)
						
				elif temp1[0]=="sendall" :
					
						x.send(temp)
						
				else:
					print ('Error Command')

				sys.stdout.write('## '); sys.stdout.flush() 

client()
