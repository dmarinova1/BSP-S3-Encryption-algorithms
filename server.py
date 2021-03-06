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


#ROT13 (de)encryption function
#initialization of letters (ASCII table where A-Z in 65-90 and a-z in 97 to 122; numbers and symbols are immune to ROT13 operations)
LOWER_LETTERS = [chr(x) for x in range(97, 123)]
UPPER_LETTERS = [chr(x) for x in range(65, 91)]


def rot13(plaintext):

    ciphertext = " "
    for char in plaintext:
        if char.isupper():
            ciphertext += encrypt_rot13(char, UPPER_LETTERS)
        elif char.islower():
            ciphertext += encrypt_rot13(char, LOWER_LETTERS)
        else:
            ciphertext += char
    return ciphertext


def encrypt_rot13(char, alphabet):
    newChar = ''
    originalIndex = alphabet.index(char)
    newIndex = originalIndex + 13 #each letter rotated 13 characters
    newChar += alphabet[newIndex % len(alphabet)]
    return newChar


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

    choice2 = int(input("1.Decryption with Caeser cipher\n2.Decryption with ROT13\n3.Decryption with AES\n4.Decryption with DES\n5.Close connection\nChoose 1,2,3,4 or 5: "))
        
        
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
        message = incoming_message
        print("---Decrypting with ROT13---")
        start = time()
        decrypted_text = rot13(message)
        print(decrypted_text)
        end = time()
        conn.send(decrypted_text.encode())
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

        desinput = bytes.fromhex(incoming_message)
        start = time()
        decrypted_text = des.decrypt(desinput).decode("utf-8").rstrip() #rstrip() unpads the recovered cleartext
        print("The cleartext is: '" + decrypted_text+"'")
        end = time()
        conn.send(decrypted_text.encode())
        print("Message sent.")
        print("")
        print("It took %f seconds." % (end - start))
    
    elif choice2 == 5:
        break
    else:
        print("Invalid choice")
            
            
conn.close()
