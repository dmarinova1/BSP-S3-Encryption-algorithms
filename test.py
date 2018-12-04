import base64
import hashlib, os
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome import Random
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import unpad
from timeit import default_timer as time



def despad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text


def make_key(aespassword):

    key = hashlib.sha256(aespassword.encode("utf-8")).digest()
    return key

def aesencrypt(message, key):
	
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


def aesdecrypt(ciphertext, key):

    enc_msg = base64.b64decode(ciphertext)
    fin_iv = open("iv.dat", "rb")
    iv = fin_iv.read()
    fin_iv.close()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = unpad(cipher.decrypt(enc_msg), 16)
    return msg.decode("utf-8")

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


def encrypt_rot13():
    message = input("Enter you message to be encrypted: ").upper()

    key = 13
    encrypt_text = ""
    for i in range(len(message)):
        temp = ord(message[i]) + key
        if ord(message[i]) == 32:
            encrypt_text += " "
        elif temp > 90:
            temp -= 26
            encrypt_text += chr(temp)
        else: 
            encrypt_text += chr(temp)


    print("Encrypted message using ROT13:", encrypt_text)


def decrypt_rot13():
    message = input("Enter you message to be decrypted: ").upper()

    key = 13
    decrypt_text = ""
    for i in range(len(message)):
        temp = ord(message[i]) - key
        if ord(message[i]) == 32:
            decrypt_text += " "
        elif temp < 65:
            temp += 26
            decrypt_text += chr(temp)
        else:
            decrypt_text += chr(temp)
  

    print("Decrypted message using ROT13: ", decrypt_text)



def main():
    while True:
        eOrD = str(input("Are you trying to encrypt or decrypt a message? "))

        
        if eOrD == "encrypt" or eOrD == "e":
            while True: 
                choice1 = int(input("1.Encryption with Caeser cipher\n2.Encryption with ROT13\n3.Encryption with AES\n4. Encryption with DES\n5.Go back\nChoose 1,2, 3, 4 or 5: "))
                if choice1 == 1:
                    text1 = input("What is the message you would like to have encrypted?: ")
                    print("---Encrypting with Caeser cipher---")
                    start = time()
                    print(encryptCaeser(text1))
                    end = time()
                    print("It took %f seconds." % (end - start))


                elif choice1 == 2:
                    print("---Encrypting with ROT13---")
                    start = time()
                    encrypt_rot13()
                    end = time()
                    print("It took %f seconds." % (end - start))

                elif choice1 == 3:
                    aespassword = input("Enter AES encryption password: ")
                    aesinput1 = input("Enter your message to be encrypted: ")
                    key = make_key(aespassword)
                    start = time()
                    ciphertext = aesencrypt(aesinput1, key)
                    print(b"The ciphertext is: " + ciphertext)
                    end = time()
                    print("It took %f seconds." % (end - start))
                    
                    # Write the cipher and the key in separate files
                    fout_cipher = open("cipher.dat", "wb")
                    fout_cipher.write(ciphertext)
                    fout_cipher.close()
                    
                    fout_key = open("key.dat", "wb")
                    fout_key.write(key)
                    fout_key.close()
                
                elif choice1 == 4:
                    key = "mysecret"
                    des = DES.new(key.encode("utf-8"), DES.MODE_ECB)
                    text1 = input("Enter your message: ")
                    padded_text = despad(text1)
                    start = time()
                    encrypted_text = des.encrypt(padded_text.encode("utf-8"))
                    print(encrypted_text)
                    end = time()
                    print("It took %f seconds." % (end - start))
                
                elif choice1 == 5:
                    break

                else:
                    print("Invalid choice")

        if eOrD == "decrypt" or eOrD == "d":
            while True:
                choice2 = int(input("1.Decryption with Caeser cipher\n2.Decryption with ROT13\n3. Decryption with AES\n4.Decryption with DES\n5.Go back\nChoose 1,2,3,4 or 5: "))
                if choice2 == 1:
                    text2 = input("Enter message to be decrypted: ")
                    print("---Decrypting with Caeser cipher---")
                    start = time()
                    print(decryptCaeser(text2))
                    end = time()
                    print("It took %f seconds." % (end - start))



                elif choice2 == 2:
                    print("---Decrypting with ROT13---")
                    start = time()
                    decrypt_rot13()
                    end = time()
                    print("It took %f seconds." % (end - start))

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
                    print("AM: The clear text is: " + decrypted)
                    end = time()
                    print("It took %f seconds." % (end - start))
                    
                
                elif choice2 == 4:
                    key = "mysecret"
                    des = DES.new(key.encode("utf-8"), DES.MODE_ECB)
                    desinput = input("Enter your message to be encrypted and decrypted: ")
                    padded_text = despad(desinput)
                    start = time()
                    encrypted_text = des.encrypt(padded_text.encode("utf-8"))
                    print(b"Given encrypted message: " + encrypted_text)
                    print("The cleartext is: " + des.decrypt(encrypted_text).decode("utf-8"))
                    end = time()
                    print("It took %f seconds." % (end - start))

                elif choice2 == 5:
                    break
                else:
                    print("Invalid choice")
        else: 
            print("Please enter the word 'encrypt' or the word 'decrypt'")


if __name__ == "__main__":
    main()
