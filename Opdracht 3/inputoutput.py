def inputoutputfunc(invoernaam, uitvoernaam, boodschap):
    with open(invoernaam, 'r') as invoerbestand:
        print(invoerbestand.read())
    with open(uitvoernaam, 'a+') as uitvoerbestand:
        uitvoerbestand.write(boodschap + '\n')

invoernaam = input()
uitvoernaam = input()
boodschap = input()
inputoutputfunc(invoernaam, uitvoernaam, boodschap)