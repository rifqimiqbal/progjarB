import sys
import socket
import select
import string

SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096

HOST = 'localhost'
PORT = 8080

def server():

	# membuat TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# menghubungkan socket
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# menambahkan server socket object ke list readable connections
	SOCKET_LIST.append(server_socket)

	print "Menunggu client..."

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

		for sock in ready_to_read:
			# when new connection request received
			if sock == server_socket: # cek kalau socketnya sesuai dengan socket server
				sockfd, addr = server_socket.accept() # socket & addr client baru di-accept
				SOCKET_LIST.append(sockfd) # push sockfd baru ke array
				print "Client (%s, %s) terhubung" % addr

				broadcast(server_socket, sockfd, "(%s, %s) telah bergabung ke dalam ruang chat\n" % addr)
			 
			# a message from a client, not a new connection
			else:
				# process data received from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					if data:
						temp1 = string.split(data[:-1])

						d=len(temp1)
						if temp1[0]=="login" :
							log_in(sock, str(temp1[1]))

						elif temp1[0]=="send" :
							login = 0
							user = ""
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									login = 1
									user=NAME_LIST[x+1]

							if login==0:
								send_msg(sock, "Login terlebuh dahulu\n")

							else:
								temp2=""
								for x in range (len(temp1)):
									if x>1:
										if not temp2:
											temp2+=str(temp1[x])
										else:
											temp2+=" "
											temp2+=str(temp1[x])
								
								for x in range (len(NAME_LIST)):
									if NAME_LIST[x]==temp1[1]:
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n")

						elif temp1[0]=="list" :
							login = 0
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									login = 1
							
							if login==0:
								send_msg(sock, "Login terlebih dahulu\n")
							
							else:
								temp2=""
								for x in range (len(NAME_LIST)):
									if x%2==1:
										temp2+=" "
										temp2+=str(NAME_LIST[x])
								send_msg(sock, "(List): "+temp2+"\n")
		
						elif temp1[0]=="sendall" :
							
							login = 0
							user = ""
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									login=1
									user=NAME_LIST[x+1]
							
							if login==0:
								send_msg(sock, "Please login first\n")
							
							else:
								temp2=""
								for x in range(len(temp1)):
									if x!=0:
										if not temp2:
											temp2=str(temp1[x])
										else:
											temp2+=" "
											temp2+=temp1[x]
								broadcast(server_socket, sock, "["+user+"]: "+temp2+"\n")

						else:
							print ('Perintah salah')
					else:
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "Client (%s, %s) sedang offline\n" % addr) 

				# exception 
				except:
					broadcast(server_socket, sock, "Client (%s, %s) sedang offline\n" % addr)
					continue

	server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for x in range (len(NAME_LIST)):
		
        # send the message only to peer
        if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 :
            try :
                NAME_LIST[x].send(message)
            except :
                # broken socket connection
                NAME_LIST[x].close()
                # broken socket, remove it
                if NAME_LIST[x] in SOCKET_LIST:
                    SOCKET_LIST.remove(NAME_LIST[x])
 
def send_msg (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock)

def log_in (sock, user):
	u = 0
	s = 0
	for name in NAME_LIST:
		if name == user: u = 1
		if name == sock: s = 1
	
	if s==1:
		send_msg(sock, "Anda sudah memiliki username\n")
	elif u==1:
		send_msg(sock, "Username sudah ada yang punya\n")
	else:
		NAME_LIST.append(sock)
		NAME_LIST.append(user)
		send_msg(sock, "Login berhasil\n")
	
server()
