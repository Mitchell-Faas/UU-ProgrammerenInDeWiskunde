def roman2int(str):
    translation_dict = {'M': 1000,
                         'D': 500,
                         'C': 100,
                         'L': 50,
                         'X': 10,
                         'V': 5,
                         'I': 1}

    total = 0
    for i, char in enumerate(str):
        try:
            # Check if next is larger
            if translation_dict[str[i+1]] > translation_dict[char]:
                # If so, subtract TWICE the value
                # (we'll be adding 1x the value later.)
                total -= 2* translation_dict[char]
        except IndexError:
            pass
        finally:
            total += translation_dict[char]

    return total


def int2roman(num):
    translation_tuple = ((1000, 'M'),
                          (900, 'CM'),
                          (500, 'D'),
                          (400, 'CD'),
                          (100, 'C'),
                           (90, 'XC'),
                           (50, 'L'),
                           (40, 'XL'),
                           (10, 'X'),
                            (9, 'IX'),
                            (5, 'V'),
                            (4, 'IV'),
                            (1, 'I'))

    output = ''

    # Go through every pair in order
    for pair in translation_tuple:
        # Get divisor and remainder
        times, num = divmod(num, pair[0])

        # Add to output
        output += pair[1] * times

    return output

if __name__ == "__main__":
    st = """I
    II
    III
    IV
    V
    VI
    VII
    VIII
    IX
    X
    XI
    XII
    XIII
    XIV
    XV
    XVI
    XVII
    XVIII
    XIX
    XX
    XXI
    XXII
    XXIII
    XXIV
    XXV
    XXVI
    XXVII
    XXVIII
    XXIX
    XXX
    XXXI
    XXXII
    XXXIII
    XXXIV
    XXXV
    XXXVI
    XXXVII
    XXXVIII
    XXXIX
    XL
    XLI
    XLII
    XLIII
    XLIV
    XLV
    XLVI
    XLVII
    XLVIII
    XLIX
    L
    LI
    LII
    LIII
    LIV
    LV
    LVI
    LVII
    LVIII
    LIX
    LX
    LXI
    LXII
    LXIII
    LXIV
    LXV
    LXVI
    LXVII
    LXVIII
    LXIX
    LXX
    LXXI
    LXXII
    LXXIII
    LXXIV
    LXXV
    LXXVI
    LXXVII
    LXXVIII
    LXXIX
    LXXX
    LXXXI
    LXXXII
    LXXXIII
    LXXXIV
    LXXXV
    LXXXVI
    LXXXVII
    LXXXVIII
    LXXXIX
    XC
    XCI
    XCII
    XCIII
    XCIV
    XCV
    XCVI
    XCVII
    XCVIII
    XCIX
    C"""

    for line in st.splitlines():
        print(roman2int(line))

    for i in range(101):
        print(int2roman(i))