import socket



ip = input('Enter the IP address: ')
print(ip)
port = 1234

#create a socket as communication endpoint using the TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #connect the client's socket with the server's socket as the given IP and port number
    s.connect((ip, port))
    #send some data and get the server's reply
    s.sendall(b"Hello, world!")
    data = s.recv(1024)
    print("received: ", data)
    #send some other data and receive the reply
    s.sendall(b"Hello again!")
    data = s.recv(1024)
    print("received: ", data)
