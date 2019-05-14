inpath = input()
outpath = input()
message = input()

with open(inpath, 'r') as infile:
    print(infile.read())


with open(outpath, 'a') as outfile:
    outfile.write(message + '\n')