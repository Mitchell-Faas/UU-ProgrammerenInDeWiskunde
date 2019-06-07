adress_list = [int(x) for x in input().split()]
goal_idx = len(adress_list)//2
pivot_idx = len(adress_list)-1

# Hmmm, lekker zelfplagiaat
# Deze komt van de sorteer.py opdracht uit week 5
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

def quickselect(list, low, high):
    if low < high:
        # Sorteer met partition, en herhaal dan met de gesplitste lijsten
        p = partition(list, low, high)
        if p > goal_idx:
            quickselect(list, low, p-1)
        if p < goal_idx:
            quickselect(list, p+1, high)

"""
while pivot_idx != goal_idx:
    if
    pivot_idx = partition(adress_list, 0, pivot_idx)
"""
quickselect(adress_list, 0, pivot_idx)
# Henk woont in het midden
h = (max(adress_list[:goal_idx]) + min(adress_list[goal_idx:])) // 2

afstand = 0
for adress in adress_list:
    afstand += abs(adress-h)
print(afstand)