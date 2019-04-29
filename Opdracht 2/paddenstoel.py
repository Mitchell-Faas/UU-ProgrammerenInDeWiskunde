def lekkerofniet(shade, length, spotdensity):
    # Any shade < 0.5 returns 1
    if shade <= 0.5:
        return 1
    # From hereon out we can assume shade > 0.5

    # Any length not between 0.25 and 0.75 is blue.
    if not (0.25 < length < 0.75):
        return 2
    # From hereon out we can assume 0.25 < length < 0.75

    # Spotdensity separates the rest in to thirds
    if spotdensity < 1/3:
        return 3
    elif spotdensity < 2/3:
        return 4

    # Every test has been done and purple is all that remains
    return 5


# Check if we're imported or running alone
if __name__ == '__main__':
    input = [float(x) for x in input().split(',')]

    # Using the star operator to unpack input
    print(lekkerofniet(*input))