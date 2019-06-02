# Based on https://en.wikipedia.org/wiki/Quicksort, https://www.youtube.com/watch?v=MZaf_9IZCrc
from random import randint
from math import ceil
import cProfile as pr
from sys import setrecursionlimit
from timeit import timeit

setrecursionlimit(10000)
def quicksort(list, low, high):
    if low < high:
        # Sorteer met partition, en herhaal dan met de gesplitste lijsten
        p = partition(list, low, high)
        quicksort(list, low, p-1)
        quicksort(list, p+1, high)

def partition(list, low, high):
    # Kies het laatste element als referentiepunt
    pivot = list[high]
    i = low
    swap = False
    # Als alles al in volgorde staat moet je de pivot niet verplaatsen
    for j in range(low,high):
        if list[j] < pivot:
            # Als deze lager is dan de pivot, swap hem naar het 'lage' deel van de lijst, afgebakend door i
            list[i], list[j] = list[j], list[i]
            # Verplaats i zodat hij nog steeds het 'lage' deel afbakent
            i += 1
        else:
            # Er is een element links van de pivot die groter is dan de pivot, we moeten ze zo verruilen
            swap = True
    if swap:
        # Stop de pivot op de juiste plek in de lijst. Swap zo mogelijk met de eerste entry die hoger is
        list[i], list[high] = list[high], list[i]
    return i


def mathcontest(hardlist, smartlist):
    listlen = len(hardlist)
    # Sorteer beide lijsten
    quicksort(hardlist, 0, listlen - 1)
    quicksort(smartlist, 0, listlen - 1)
    # Als er niks fout gaat is het mogelijk
    output = 'mogelijk'
    for idx in range(listlen):
        # Check voor elke entry of de opdracht te makkelijk of te moeilijk is
        if hardlist[idx] < ceil(smartlist[idx]/2) or hardlist[idx] > smartlist[idx]:
            # Als het fout gaat, stop meteen en zet output naar 'onmogelijk'
            output = 'onmogelijk'
            break
    return(output)

for idx in range(7):
    testhardlist = [randint(0,100) for x in range(10**idx)]
    testsmartlist = [randint(0,100) for x in range(10**idx)]
#print(mathcontest(testhardlist, testsmartlist))
#pr.run("mathcontest(testhardlist, testsmartlist)")

    print(timeit("mathcontest(testhardlist,testsmartlist)",number=1,globals=globals()))

#hardlist = [int(x) for x in input().split()]
#smartlist = [int(x) for x in input().split()]
#print(mathcontest(hardlist, smartlist))