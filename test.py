import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16

def pad(s): 
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): 
    #return s[:-ord(s[len(s) - 1:])]
    return s[0:-s[-1]]


def aesencrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest() #to avoid getting ValueError when the password is not 16 bytes (but another amount of bytes) or not dividable by 16, hence the key/password must be hashed 
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))


def aesdecrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    print(iv)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    print(bytes.fromhex(cipher.decrypt(enc).decode('utf-8')))
    return unpad(cipher.decrypt(enc[16:])).decode('utf-8')



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
    message = message.upper()
    key = 3
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alphalen = len(alphabet)
    newMessage = ""
    for char in message:
        if char in alphabet:
            position = alphabet.find(char)
            position -= key
            if position >= alphalen:
                position = position-alphalen
            elif position < 0:
                position += alphalen
                newMessage += alphabet[position]
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
                choice1 = int(input("1.Encryption with Caeser cipher\n2.Encryption with ROT13\n3.Encryption with AES\n4.Go back\nChoose 1,2, 3 or 4: "))
                if choice1 == 1:
                    text1 = input("What is the message you would like to have encrypted?: ")
                    print("---Encrypting with Caeser cipher---")
                    print(encryptCaeser(text1))

                elif choice1 == 2:
                    print("---Encrypting with ROT13---")
                    encrypt_rot13()

                elif choice1 == 3:
                    aespassword = input("Enter AES encryption password: ")
                    aesinput1 = input("Enter your message to be encrypted: ")
                    encrypted = aesencrypt(aesinput1, aespassword)
                    print(encrypted)
                
                elif choice1 == 4:
                    break

                else:
                    print("Invalid choice")

        if eOrD == "decrypt" or eOrD == "d":
            while True:
                choice2 = int(input("1.Decryption with Caeser cipher\n2.Decryption with ROT13\n3. Decryption with AES\n4.Go back\nChoose 1,2,3 or 4: "))
                if choice2 == 1:
                    text2 = input("Enter message to be decrypted: ")
                    print("---Decrypting with Caeser cipher---")
                    print(decryptCaeser(text2))
                elif choice2 == 2:
                    print("---Decrypting with ROT13---")
                    decrypt_rot13()
                elif choice2 == 3:
                    aespassword = ("Enter AES password: ")
                    aesinput2 = input("Enter message to be decrypted: ")
                    decrypted = aesdecrypt(aesinput2,aespassword)
                    print(decrypted)
                    #print(bytes.decode(decrypted))

                elif choice2 == 4:
                    break
                else:
                    print("Invalid choice")
        else: 
            print("Please enter the word 'encrypt' or the word 'decrypt'")


if __name__ == "__main__":
    main()
