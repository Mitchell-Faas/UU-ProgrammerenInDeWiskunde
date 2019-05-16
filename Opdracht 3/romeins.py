
int2romandict = {'1':'I','2':'II','3':'III','4':'IV','5':'V','6':'VI','7':'VII','8':'VIII','9':'IX','10':'X'}

def int2roman(integer):
    # Deze code is fout
    left = int(integer)
    outputstr = ''
    while left > 0:
        if left >= 1000:
            outputstr += 'M'
            left = left-1000
        elif left >= 900:
            outputstr += 'CM'
            left = left - 900
        elif left >= 500:
            outputstr += 'D'
            left = left - 500
        elif left >= 400:
            outputstr += 'CD'
            left = left - 400
        elif left >= 100:
            outputstr += 'C'
            left = left - 100
        elif left >= 90:
            outputstr += 'XC'
            left = left - 90
        elif left >= 50:
            outputstr += 'L'
            left = left - 50
        elif left >= 40:
            outputstr += 'XL'
            left = left - 40
        elif left >= 10:
            outputstr += 'X'
            left = left - 10
        else:
            outputstr += int2romandict[str(left)]
            break


    return outputstr


roman2intdict = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}

def roman2int(romanstring):
    counter = 0
    length = len(romanstring)
    for idx in range(length-1): # Add or subtract each number except the last one \
        # depending on whether it's larger or smaller compared to the following number.
        currentnumber = roman2intdict[romanstring[idx]]
        nextnumber = roman2intdict[romanstring[idx+1]]
        if currentnumber < nextnumber:
            counter -= currentnumber
        else:
            counter += currentnumber
    counter += roman2intdict[romanstring[-1]]# Add the last number

    return counter
