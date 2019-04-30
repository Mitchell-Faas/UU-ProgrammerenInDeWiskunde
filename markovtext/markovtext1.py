import random
from collections import Counter

dictall = {}
dictstart = {}

with open('navysealcopypasta.txt','r') as file:

    for line in file:
        wordlist = line.split(' ')
        # Als er laatste regel een woord geskipt is, voeg hem hier alsnog toe in de dictionary
        if lastword:
            dictall.setdefault(lastword, Counter())
            dictall[lastword][wordlist[0]] += 1
        # Voeg alle woorden van deze line toe aan de dictionary
        for idx, word in enumerate(wordlist):
            dictall.setdefault(word, Counter())
            if idx < wordlist.__len__():
                # Next word exists so just do normal stuff
                dictall[word][wordlist[idx+1]] += 1
            else:
                # End of line; oh oh
                lastword = word





#wordlist = text.split(' ')


dict = {}
for x in range(len(wordlist)-1):
    dict.setdefault(wordlist[x], [])
    dict[wordlist[x]].append(wordlist[x+1])

lastword = 'What'
markovsentence = lastword
maxlength = 60

for i in range(maxlength):
    lastword = random.choice(dict[lastword])
    markovsentence += ' ' + lastword
    if '?' in markovsentence or '.' in markovsentence:
        break

print(markovsentence)
