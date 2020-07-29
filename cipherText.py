#Text encrypter
#Seth Raphael
#Created 5/2/2020
#Initialize the empty lists where the text will go
text = []
ciphertext = []
#Create the function that encrypts the text
def cipherText(words):
    #Loop through every letter in the text
    for char in words:
        #If it's at the end of the alphabet bring it to the beginning
        if char == "X" or char == "Y" or char == "x" or char == "y" or char == "z" or char == "Z":
            intValue = ord(char)
            convInt = intValue - 23
            letter = chr(convInt)
            ciphertext.append(letter)
        #Keep the special characters the same
        elif char == " " or char == "!" or char == "#" or char == "$" or char == "%" or char == "&" or char == "'":
            ciphertext.append(char)
        elif char == "(" or char == ")" or char == "*" or char == "+" or char == "," or char == "-" or char == ".":
            ciphertext.append(char)
        elif char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6":
            ciphertext.append(char)
        elif char == "7" or char == "8" or char == "9" or char == ":" or char == ";" or char == "<" or char == "=":
            ciphertext.append(char)
        elif char == ">" or char == "?" or char == "@" or char == "^" or char == "~" or char == "`" or char == "/":
            ciphertext.append(char)
        elif char == "_" or char == "{" or char == "}" or char == "[" or char == "]":
            ciphertext.append(char)
        #Encrypt the main text
        else:
            intValue = ord(char)
            convInt = intValue + 3
            letter = chr(convInt)
            ciphertext.append(letter)
    #Print the encrypted text
    print(*ciphertext)
#Create the function that decrypts the text
def normalText(ciphertext):
    #Loop through every letter in the encryption
    for char in ciphertext:
        #If it's at the beginning of the alphabet bring it to the end
        if char == "A" or char == "B" or char == "C" or char == "a" or char == "b" or char == "c":
            intValue = ord(char)
            convInt = intValue + 23
            letter = chr(convInt)
            text.append(letter)
        #Keep the special characters the same
        elif char == " " or char == "!" or char == "#" or char == "$" or char == "%" or char == "&" or char == "'":
            text.append(char)
        elif char == "(" or char == ")" or char == "*" or char == "+" or char == "," or char == "-" or char == ".":
            text.append(char)
        elif char == "0" or char == "1" or char == "2" or char == "3" or char == "4" or char == "5" or char == "6":
            text.append(char)
        elif char == "7" or char == "8" or char == "9" or char == ":" or char == ";" or char == "<" or char == "=":
            text.append(char)
        elif char == ">" or char == "?" or char == "@" or char == "^" or char == "~" or char == "`" or char == "/":
            text.append(char)
        elif char == "_" or char == "{" or char == "}" or char == "[" or char == "]":
            text.append(char)
        #Decrypt the main text
        else:
            intValue = ord(char)
            convInt = intValue - 3
            letter = chr(convInt)
            text.append(letter)
    #Print the decrypted text
    print(*text)
#Ask the user what they would like to encrypt
words = input("What would you like to encrypt? >>> ")
#Call the encryption function
cipherText(words)
#Ask the user if they would like to decrypt their message
decrypt = input("Would you like to decrypt your message? Y/N >>> ")
if decrypt == "Y":
    #Call the decryption function
    normalText(ciphertext)
elif decrypt == "N":
    #End the program if they don't want to decrypt
    print("Ok. Have a nice day!")
