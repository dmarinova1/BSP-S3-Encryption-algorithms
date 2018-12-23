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

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = str(socket.gethostbyname(socket.gethostname()))
port = 1234
s.connect((host,port))
print("Connected to chat server")

# Caesar cipher encryption function
def encryptCaeser(message):
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = 3
    newMessage = ""

    for char in message:
        if char in alphabet:
            position = alphabet.find(char)
            newPosition = (position + key) % 26
            newChar = alphabet[newPosition]
            newMessage += newChar
        else:
            newMessage += char
    return newMessage


#ROT13 encryption function
#initialization of letters (ASCII table where A-Z in 65-90 and a-z in 97 to 122; numbers and symbols are immune to ROT13 operations)
LOWER_LETTERS = [chr(x) for x in range(97, 123)]
UPPER_LETTERS = [chr(x) for x in range(65, 91)]


def rot13(message):

    ciphertext = " "
    for char in message:
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


#AES key/password creation followed by encryption function
def make_key(aespassword):

    key = hashlib.sha256(aespassword.encode("utf-8")).digest()
    return key


def aesencrypt(message, key):
    #   before encrypting a plaintext of X bytes, we append to the back as many bytes we need to to reach the next 16 byte boundary.
    pad = AES.block_size - len(message) % AES.block_size
    try:
        message = message.decode()
    except:
        pass
    message = message + pad * chr(pad)

    iv = os.urandom(16)
    fout_iv = open("iv.dat", "wb")
    fout_iv.write(iv)
    fout_iv.close()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(message.encode("utf-8"))
    print(ciphertext)
    ciphertext = base64.b64encode(ciphertext)

    return ciphertext

#DES padding
def despad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text





while True:
    key = "mysecret"
    des = DES.new(key.encode("utf-8"), DES.MODE_ECB)

    choice1 = int(input("1.Encryption with Caeser cipher\n2.Encryption with ROT13\n3.Encryption with AES\n4.Encryption with DES\n5.Close connection\nChoose 1,2,3,4 or 5: "))
    if choice1 == 1:
        message = input("Enter your message to be encrypted: ")
        print("---Encrypting with Caeser cipher---")
        start = time()
        encrypted_text = encryptCaeser(message)
        print(encrypted_text)
        end = time()
        s.send(encrypted_text.encode())
        print("Message sent.")
        print("")
        print("Encryption with Caeser cipher took %f seconds." % (end - start))

    elif choice1 == 2:
        message = input("Enter your message to be encrypted: ")
        print("---Encrypting with ROT13---")
        start = time()
        encrypted_text = rot13(message)
        print(encrypted_text)
        end = time()
        s.send(encrypted_text.encode())
        print("Message sent.")
        print("")
        print("Encryption with ROT13 took %f seconds." % (end - start))
            
    elif choice1 == 3:
        aespassword = input("Enter AES encryption password: ")
        aesinput1 = input("Enter your message to be encrypted: ")
        key = make_key(aespassword)
        start = time()
        ciphertext = aesencrypt(aesinput1, key)
        print(b"The ciphertext is: " + ciphertext)
        end = time()
        s.send(ciphertext)
        print("Message sent.")
        print("")
        print("Encryption with AES took %f seconds." % (end - start))

        # Write the cipher and the key in separate files
        fout_cipher = open("cipher.dat", "wb")
        fout_cipher.write(ciphertext)
        fout_cipher.close()

        fout_key = open("key.dat", "wb")
        fout_key.write(key)
        fout_key.close()

    elif choice1 == 4:
        text1 = input("Enter your message to be encrypted: ")
        padded_text = despad(text1)
        start = time()
        encrypted_text = des.encrypt(padded_text.encode("utf-8")).hex()
        print(encrypted_text)
        end = time()
        s.send(encrypted_text.encode())
        print("Message sent.")
        print("")
        print("It took %f seconds to encrypt the message using DES." % (end - start))

    elif choice1 == 5:
        break

    else:
        print("Invalid choice")

    incoming_message = s.recv(4096)
    incoming_message = incoming_message.decode()
    print(" Server : ", incoming_message.lower())
    print("")

s.close()
