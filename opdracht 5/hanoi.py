def flip(zetstring, flipdir):
    output = ''
    if flipdir == 1:
        for char in zetstring:
            if char is 'A':
                output += 'B'
            if char is 'B':
                output += 'C'
            if char is 'C':
                output += 'A'
    if flipdir == -1:
        for char in zetstring:
            if char is 'A':
                output += 'C'
            if char is 'B':
                output += 'A'
            if char is 'C':
                output += 'B'
    return output

def hanoi_iteratief(n):
    zetten = []
    # Bepaal de eerste zet, ofwel AB of AC, afhankelijk van de parity van n
    if n % 2 == 0:
        midentry = 'AC'
        notmidentry = 'AB'
        flipdir = 1
    else:
        midentry = 'AB'
        notmidentry = 'AC'
        flipdir = -1
    # De volgende middenste zet is AB als de vorige middenste zet AC was en andersom
    # Kopieer de zetten aan beide kanten van deze middenste, maar verander A, B en C \
    # door ze allemaal een plaats te verschuiven
    # de verschuivingsrichting wisselt steeds per stap
    for copyidx in range(n):
        midentry, notmidentry = notmidentry, midentry
        flipdir = flipdir*(-1)
        zetten = zetten + [midentry] + [flip(zet,flipdir) for zet in zetten]
    return(zetten)

outputstr = ''
for x in hanoi_iteratief(int(input())):
    outputstr += x + ','
outputstr = outputstr[:-1]
print(outputstr)