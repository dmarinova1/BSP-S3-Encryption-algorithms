import socket
import threading

# creates a variable ip which holds the ip of the machine it is running on
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

class EchoThread (threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        with conn:
            print("connected by", addr, "in thread",threading.current_thread())
            #keep echoing what the client sent, until the connection is closed then the EchoThread terminates
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                conn.sendall(b'you said: ' + data)
        print("connection closed with ", addr)
#we close socket connection between server and client
#create a socket as communication endpoint using the TCP protocol
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created.")
    # bind the socket to the given IP (localhost) and port number
    #listen for incoming connections (limited to 10)
s.bind((ip, port))
print("Socket has been bounded.")
s.listen(10)
print("The server is ready...")
print("IP address of the server:%s" % ip)
    
#keep accepting incoming connections in an infinite loop; create and launch a separate dedicated EchoThread to handle the communication with some client
    
while True:
    (conn, addr) = s.accept()
    print('%s connected to the server' % str(addr))
    echoThread = EchoThread(conn, addr)
    echoThread.start()
