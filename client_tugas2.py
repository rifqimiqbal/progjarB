import sys, socket, select
 
def chat_client():
    if(len(sys.argv) < 3) :
       
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    
   
    print 'tulis "pesan" '
    #sys.stdout.write(' name  '); sys.stdout.flush()
    a=raw_input()
    #s.send(test)
    if a == "pesan" :
	    sys.stdout.write(' nama  '); sys.stdout.flush()
	    a =raw_input()
	    if a == '':
	    	sys.exit()
	    try :
        	s.connect((host, port))
    	    except :
        	print 'Unable to connect'
        	sys.exit()
	    print ' pesan'
	    sys.stdout.write(a+" jawab "); sys.stdout.flush()
	    s.send(a+" jawab "+ a)   
	    while 1:
		socket_list = [sys.stdin, s]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		 
		for sock in read_sockets:            
		    if sock == s:
		        d= sock.recv(4096)
		        if not d :
		            
		            sys.exit()
		        else :
		            sys.stdout.write(d)
		            sys.stdout.write(a+" says "); sys.stdout.flush()     
		    
		    else :
		        msg = sys.stdin.readline()
			msg = a+" jawab "+msg
		        s.send(msg)
		        sys.stdout.write(a+" jawab"); sys.stdout.flush() 
    else  :
	sys.exit()
if __name__ == "__main__":

    sys.exit(chat_client())
