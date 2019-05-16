srctext = input()
codeword = input()

#Make the necessary dictionaries
letter_to_int_Dict = {}
int_to_letter_Dict = {}
alphabet = 'abcdefghijklmnopqrstuvwxyz'
for idx in range(26):
    letter_to_int_Dict[alphabet[idx]] = idx
    int_to_letter_Dict[str(idx)] = alphabet[idx]


modulo = len(codeword)
outstring = ''
for idx in range(len(srctext)):
    shiftint = letter_to_int_Dict[codeword[idx % modulo]]
    srcint = letter_to_int_Dict[srctext[idx]]
    outstring += int_to_letter_Dict[str((srcint - shiftint)%26)]
print(outstring)




