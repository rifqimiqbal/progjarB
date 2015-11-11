import threading
import socket
import time
import sys
             #membuka dan membaca file
def get_file(nama):
	myfile = open(nama)
	return myfile.read()


class MemprosesClient(threading.Thread):     #membuat thread
	def __init__(self,client_socket,client_address,nama):
		self.client_socket = client_socket
		self.client_address = client_address
		self.nama = nama
		threading.Thread.__init__(self)
	def run(self):
		while True:
			message = ''
			data = self.client_socket.recv(32)
			if data :
				message = message + data #collect seluruh data yang diterima
				print message
				                 #membaca pesan yang tertulis di tab web address jika halaman utama (localhost:2222) maka akan tampil gambar img.jpg
				if (message.endswith("\r\n\r\n")):
					self.client_socket.send(get_file('img.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman localhost:2222/barca.jpg maka akan tampil gambar 1.jpg
				elif (message.startswith("GET /barca.jpg")):
					self.client_socket.send(get_file('1.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman localhost:2222/madrid.jpg maka akan tampil gambar 2.jpg
				elif (message.startswith("GET /madrid.jpg")):
					self.client_socket.send(get_file('2.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman  localhost:2222/mu.jpg maka akan tampil gambar 3.jpg
				elif (message.startswith("GET /mu.jpg")):
					self.client_socket.send(get_file('3.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman localhost:2222/milan.jpg maka akan tampil gambar 4.jpg
				elif (message.startswith("GET /milan.jpg")):
					self.client_socket.send(get_file('4.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman localhost:2222/inter.jpg maka akan tampil gambar 5.jpg
				elif (message.startswith("GET /inter.jpg")):
					self.client_socket.send(get_file('5.jpg'))
					break
                    #membaca pesan yang tertulis di tab web address jika halaman localhost:2222/juve.jpg maka akan tampil gambar 6.jpg
                elif (message.startswith("GET /juve.jpg")):
					self.client_socket.send(get_file('6.jpg'))
					break
			else:
				break

		self.client_socket.close()  #menutup koneksi socket

class Server(threading.Thread):
	def __init__(self):
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost',2222)      #webserver berjalan pada localhost:2222
		self.my_socket.bind(self.server_address)
		threading.Thread.__init__(self)
	def run(self):
		self.my_socket.listen(1)
		nomor=0
		while (True):
			self.client_socket, self.client_address = self.my_socket.accept()
			nomor=nomor+1
			#---- menghandle message cari client (Memproses client)
			my_client = MemprosesClient(self.client_socket, self.client_address, 'PROSES NOMOR '+str(nomor))
			my_client.start()
			#----
serverku = Server()
serverku.start()
