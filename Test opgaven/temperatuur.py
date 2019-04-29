import sys

def main():
    temperatures = list(sys.argv[1:])

    # Ensure everything is integer
    try:
        for i in range(len(temperatures)):
            temperatures[i] = int(temperatures[i])
    except ValueError:
        raise IOError("It seems like you input a temperature that could not\n\
        be converted to an integer. Please be sure you give correct input.")

    max = temperatures[0]
    min = temperatures[0]
    max_drop = 0
    # Calculate max and min. Then subtract for final answer.
    for t in temperatures: # Move i from 1 to length of temps
        if max < t:
            # We found a new maximum, so know the drop.
            this_drop = max-min

            # Is this drop larger than the previous one?
            if this_drop > max_drop:
                max_drop = max-min

            # If we found a new maximum, the minimum needs resetting.
            max = t
            min = t

        if min > t:
            min = t

    print(max_drop)

if __name__ == "__main__":
    main()