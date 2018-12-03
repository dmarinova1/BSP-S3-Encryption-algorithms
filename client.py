import socket
import sys



ip = str(socket.gethostbyname(socket.gethostname()))
print("The IP Address is: " + ip)
port = 1234

#create a socket as communication endpoint using the TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created.")
    #connect the client's socket with the server's socket as the given IP and port number
s.connect((ip, port))
print("Socket connected to " + ip)

message = input("Type message: ")
try:
    s.sendall(message.encode()) #send some data
except socket.error:
    print("Not sent.")
    sys.exit()
print("Message sent.")
data = s.recv(4096) #get server's reply
print(data.decode())
s.close() #we close socket that allows connections to exist

