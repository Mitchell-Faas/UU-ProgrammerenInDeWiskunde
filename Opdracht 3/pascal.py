inputlist = input().split() # Take input
pos = int(inputlist[0])# Save input as integers
row = int(inputlist[1])
pascalpyramid = [] # Make a place to store our pyramid

for idxrow in range(row): # Create rows up to the one requested
    if idxrow == 0: # First row manually set to [1]
        pascalpyramid.append([1])
    elif idxrow == 1: # Second row manually set to [1,1]
        pascalpyramid.append([1,1])
    else:
        rowlistnew = [1] # Put a 1 at the start of the row
        for idxpos in range(1, idxrow): # Add together entries from the previous row to get new entries
            entry = pascalpyramid[idxrow-1][idxpos-1] + pascalpyramid[idxrow-1][idxpos]
            rowlistnew.append(entry)
        rowlistnew.append(1) # Put a 1 at the end of the row

        pascalpyramid.append(rowlistnew) # Add the new row to the pyramid

print(pascalpyramid[row-1][pos-1]) # Because my count of rows starts at 1, but arrays start at 0, /
# we need a correction of -1