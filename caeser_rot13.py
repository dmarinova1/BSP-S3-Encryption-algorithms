def caesercipher(message):
    
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


def rot13(plaintext):
    
    ciphertext = ""

    
    for char in plaintext:
        c = ord(char)
        
        if c >= ord('a') and c <= ord('z'): 
            if c > ord('m'):
                c -= 13
            else:
                c += 13
        elif c >= ord('A') and c <= ord('Z'):
            if c > ord('M'):
                c -= 13
            else:
                c += 13

        
        char = chr(c)
        ciphertext += chr(c)

   
    return ciphertext
    

def main():

    print("Welcome to ROT13 cipher!")
    print("Welcome to Caeser cipher!")

    while True:
        text1 = input("Please enter your message for ROT13: ")
        text2 = input("Please enter your message for Caeser cipher: ")
        if len(text1 and text2) == 0:
            break
        else:
            print("ROT13:", rot13(text1))
            print("Caeser cipher:", caesercipher(text2))
      
    
main()
