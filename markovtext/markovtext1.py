import random
from collections import Counter
import numpy as np

textFilePath = "navysealcopypasta.txt"

def dictFromFile(textFilePath):
    # Define output dictionary
    dictall = {}
    startwordlist = []
    endsentence = False

    with open(textFilePath, 'r') as file:
        for line in file:
            wordlist = line.split(' ')

            # Als er laatste regel een woord geskipt is, voeg hem hier alsnog toe in de dictionary
            try:
                dictall.setdefault(lastword, Counter())
                dictall[lastword][wordlist[0]] += 1
            except (NameError or IndexError):
                pass

            # Voeg alle woorden van deze line toe aan de dictionary
            for idx, word in enumerate(wordlist):
                dictall.setdefault(word, Counter())
                try:
                    # Next word exists so just do normal stuff
                    dictall[word][wordlist[idx+1]] += 1
                except IndexError:
                    # End of line; oh oh
                    lastword = word
                # If the previous word was the end of a sentence, add the word after it to startwordlist
                if endsentence == True:
                    startwordlist.append(word)
                    endsentence = False
                # Check whether the word is the end of a sentence
                if '?' in word or '.' in word:
                    endsentence = True

    return [dictall,startwordlist]

wordDict, startwordlist = dictFromFile(textFilePath)

for key in wordDict:
    wordDict[key] = wordDict[key].most_common()


startWord = random.choice(startwordlist)
maxLength = 60
sentenceWords = []

currentWord = startWord
writing = True
for _ in range(maxLength):
    sentenceWords.append(currentWord)

    if '?' in currentWord or '.' in currentWord:
        break

    wordarr, occurencearr = zip(*wordDict[currentWord])
    occurencearr = np.array(occurencearr)

    # Get normalizer number
    total = np.sum(occurencearr)
    # Array of probabilities
    parr = occurencearr/total

    currentWord = np.random.choice(wordarr, p=parr)

sentence = " ".join(sentenceWords)

print(sentence)
