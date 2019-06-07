from math import floor
temp_list = [int (x) for x in input().split()]
temp_diff = int((temp_list[-1] - temp_list[0]) / (len(temp_list)))
startidx = 0
endidx = len(temp_list)

while endidx - startidx > 1:
    middleidx = floor((endidx + startidx) / 2)
    if temp_list[middleidx] - temp_list[startidx] == (middleidx - startidx)*temp_diff:
        startidx = middleidx
    else:
        endidx = middleidx

print(startidx, temp_list[startidx] + temp_diff)
