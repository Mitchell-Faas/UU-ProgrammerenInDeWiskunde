# Copyright (C) 2019 Mitchell Faas
# This code must be considered confidential. No part of
# this code may be duplicated, shown, or used in any way
# without the express written permission of the Author -
# Mitchell Faas - email: Faas.Mitchell@gmail.com

from math import *


def Sieve(n: int):
    # Initialize primes array
    primes = [1]*n
    for i in range(n):
        primes[i] = i

    # Start sieving
    foundPrimes = 0
    for i in range(2,n):
        # if i isn't sieved out, discard its multiples
        if primes[i] != 0:
            foundPrimes += 1
            for j in range(2*i, n, i):
                primes[j] = 0

    # Fill primeList
    primeList = []
    for i, x in enumerate(primes[2:]): # Discard the first 2 elements (0, 1)
        if x != 0:
            primeList.append(i+2)

    return primeList


def Comb(primesSieved: list, start: int, end: int):
    # Do some type cleanup
    start = int(start)
    end = int(end)
    # Initialize checklist
    numbers = [1]*(end-start)

    # comb out the non-primes
    for prime in primesSieved:
        # x*primeList[i] - start --> needs to be positive
        pSieveSqrd = prime**2

        # Ensure we we don't try to access weird indicies
        if start > pSieveSqrd:
            # If the start is larger than psquared, define jStart
            # at the next index to cross off
            if start % prime == 0:
                jStart = start
            else:
                jStart = start + (prime - start % prime)
        else:
            jStart = pSieveSqrd

        # Do the sieving
        for j in range(jStart, end, prime):
            numbers[j - start] = 0


    # Go through the sieved list
    primesList = []
    counter = 0
    for i, x in enumerate(numbers):
        if x != 0:
            primesList.append(start+i)

    return primesList


def priemzeef(n):
    sqrt_n = floor(sqrt(n))
    sieveList = Sieve(sqrt_n + 1)

    primeList = Comb(sieveList, start=2, end=n)

    return primeList


if __name__ == '__main__':
    a = priemzeef(100)

    print(a)