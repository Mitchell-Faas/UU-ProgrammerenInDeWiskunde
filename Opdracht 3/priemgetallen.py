def priemzeef(inputnumber):
    n_max = int(inputnumber)
    sievelist = list(range(2, n_max))
    for idxprime in sievelist:
        if idxprime == 0:
            pass
        else:
            primemultiple = 2*idxprime
            while primemultiple < n_max:
                sievelist[primemultiple-2] = 0
                primemultiple += idxprime

    primelist = []
    for primecandidate in sievelist:
        if primecandidate != 0:
            primelist.append(primecandidate)

    return primelist