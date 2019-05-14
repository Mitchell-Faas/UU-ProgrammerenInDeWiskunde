# Get input
codedmessage = input()
codeword = input()

# Paste codeword after eachother
repetition = len(codedmessage)//len(codeword) + 1
codeword *= repetition

# Define variables
alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
decodedword = ''

# Go through decoding
for i in range(len(codedmessage)):
    current_alph_num = ord(codedmessage[i])-ord('a')
    codeword_alph_num = ord(codeword[i])-ord('a')

    decoded_alph_num = (current_alph_num - codeword_alph_num)%26 + ord('a')

    decodedword += chr(decoded_alph_num)

print(decodedword)