strcoord1, strcoord2 = input().split(',')
coord1 = float(strcoord1)
coord2 = float(strcoord2)
if float((52+(4+52/60)/60)) < coord1 < float((52+(5+28/60)/60)) and \
        float((5+(9+49/60)/60)) < coord2 < float((5+(11+5/60)/60)):
    print('binnen')
else:
    print('buiten')