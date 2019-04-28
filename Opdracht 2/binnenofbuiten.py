# Defining the borders in decimal form.
# (Borders are static, so no need to add conversion)
leftside = 5.16361111
rightside = 5.18472222
topside = 52.09111111
bottomside = 52.08111111

# Get input
locList = [float(x) for x in input().split(', ')]

# If inside boundaries
if (bottomside < locList[0] < topside) and \
        (leftside < locList[1] < rightside):
    print("binnen")
else:
    print("buiten")