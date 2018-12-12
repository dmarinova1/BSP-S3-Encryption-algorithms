import base64
import os
from Cryptodome import Random
from Cryptodome.Cipher import DES
from timeit import default_timer as time

def despad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def main():
    key = "mysecret"
    des = DES.new(key.encode("utf-8"), DES.MODE_ECB)

    while True:
        eOrD = str(input("Are you trying to encrypt or decrypt a message? "))

        if eOrD == "encrypt" or eOrD == "e":
            while True:
                choice1 = int(input("1.Encryption with DES\n2.Go back\nChoose 1 or 2: "))
                if choice1 == 1:
                    text1 = input("Enter your message: ")
                    padded_text = despad(text1)
                    start = time()
                    encrypted_text = des.encrypt(padded_text.encode("utf-8"))
                    encrypted_text = base64.b64encode(encrypted_text)
                    print(encrypted_text)
                    end = time()
                    print("It took %f seconds." % (end - start))
                elif choice1 == 2:
                    break

                else:
                    print("Invalid choice")

        if eOrD == "decrypt" or eOrD == "d":
            while True:
                choice2 = int(input("1.Decryption with DES\n2.Go back\nChoose 1 or 2: "))
                if choice2 == 1:
                    desinput = input(b"Enter ciphertext to be decrypted: ")
                    start = time()
                    desinput = base64.b64decode(desinput)
                    decrypted_text = des.decrypt(desinput)
                    print(b"The cleartext is: " + decrypted_text)
                    end = time()
                    print("It took %f seconds." % (end - start))

                elif choice2 == 2:
                    break
                else:
                    print("Invalid choice")
        else:
            print("Please enter the word 'encrypt' or the word 'decrypt'")


if __name__ == "__main__":
    main()
