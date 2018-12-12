import socket
import sys
import base64
import hashlib
import os
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import unpad
from timeit import default_timer as time

def decryptCaeser(message):
    message = message
    key = 3
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    newMessage = ""
    for char in message:
        if char in alphabet:
            position = alphabet.find(char)
            newPosition = (position - key) % 26
            newChar = alphabet[newPosition]
            newMessage += newChar
        
        else:
            newMessage += char
    return newMessage

def decrypt_rot13(msg):
    message = msg.upper() # work with uppercase letters
    
    key = 13
    decrypt_text = ""
    for i in range(len(message)):
        temp = ord(message[i]) - key
        if ord(message[i]) == 32: #check for space i.e. 32 is empty space in ASCII
            decrypt_text += " "
        elif temp < 65: #if temp < than uppercase A add 26 and move to Z
            temp += 26
            decrypt_text += chr(temp)
        else:
            decrypt_text += chr(temp)

    return decrypt_text


def aesdecrypt(ciphertext, key):

    enc_msg = base64.b64decode(ciphertext)
    fin_iv = open("iv.dat", "rb")
    iv = fin_iv.read()
    fin_iv.close()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(enc_msg), 16)
    return msg.decode("utf-8")


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(socket.gethostbyname(socket.gethostname()))
print(" server will start on host : ", host)
port = 1234
s.bind((host,port))
print("")
print("Host and port bounded successfully.")
print("")
print("Server is ready and waiting for incoming connections...")
print("")
s.listen(10)
conn, addr = s.accept()
print(addr, " has connected to the server and is now online.")
print("")
while True:
    key = "mysecret"
    des = DES.new(key.encode("utf-8"), DES.MODE_ECB)
    incoming_message = conn.recv(4096)
    incoming_message = incoming_message.decode()
    print(" Client : ", incoming_message)
    print("")

    choice2 = int(input("1.Decryption with Caeser cipher\n2.Decryption with ROT13\n3.Decryption with AES\n4.Decryption with DES\n5.Go back\nChoose 1,2,3,4 or 5: "))
        
        
    if choice2 == 1:
        message = incoming_message
        print("---Decrypting with Caeser cipher---")
        start = time()
        decrypted_text = decryptCaeser(message)
        print(decryptCaeser(message))
        end = time()
        conn.send(decrypted_text.encode())
        print("Message sent.")
        print("")
        print("Decryption with Caeser cipher took %f seconds." % (end - start))
                
    elif choice2 == 2:
 
        print("---Decrypting with ROT13---")
        start = time()
        decrypted = decrypt_rot13(incoming_message)
        print(decrypted.lower())
        end = time()
        conn.send(decrypted.encode())
        print("Message sent.")
        print("")
        print("Decryption with ROT13 took %f seconds." % (end - start))

    elif choice2 == 3:
        if not os.path.isfile("cipher.dat"):
            print("WARN: There is no ciphertext for decryption.")
            exit(1)
        if not os.path.isfile("key.dat"):
            print("WARN: The encryption key is missing.")
            exit(1)

        fin_cipher = open("cipher.dat", "rb")
        ciphertext = fin_cipher.read()
        fin_cipher.close()

        fin_key = open("key.dat", "rb")
        key = fin_key.read()
        fin_key.close()

        start = time()
        decrypted = aesdecrypt(ciphertext, key)
        print("The clear text is: " + decrypted)
        end = time()
        conn.send(decrypted.encode())
        print("Message sent.")
        print("")
        print("Decryption with AES took %f seconds." % (end - start))


    elif choice2 == 4:

        desinput = incoming_message
        desinput = base64.b64decode(desinput)
        start = time()
        decrypted_text = des.decrypt(desinput)
        print(b"The cleartext is: " + decrypted_text)
        end = time()
        conn.send(decrypted_text)
        print("Message sent.")
        print("")
        print("It took %f seconds." % (end - start))
    
    elif choice2 == 5:
        break
    else:
        print("Invalid choice")
            
            
