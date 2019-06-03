from math import log, ceil
import cProfile as pr
class Node():
    value = 0
    childL = None
    childR = None

"""
def inorder_write(node, value):
    if not node.value:
        if node.childL == None or node.childL.value != None:
            node.value = value
        else:
            inorder_write(node.childL)
    else:
        if node.childR != None and node.childR.value == None:
            inorder_write(node.childR, value)

def maketree(entrylist):
    height = int(log(len(entrylist)+1,2)-1)
    root = Node()
    currenthlist = [root]
    for h in range(height-1):
        for node in currenthlist:
            node.childL = Node()
            node.childR = Node()

    for entry in entrylist:
        inorder_write(root,entry)
    return root"""

"""def maketree(entrylist):
    listmiddle = ceil(len(entrylist)/2)
    root = Node()
    root.value = entrylist[listmiddle-1]
    if len(entrylist) > 1:
        root.childL = maketree(entrylist[:listmiddle - 1])
        root.childR = maketree(entrylist[listmiddle:])
    return root

def treesum(entrylist, route):
    root = maketree(entrylist)
    current_node = root
    sum = current_node.value
    for char in route:
        if char == 'L':
            current_node = current_node.childL
        if char == 'R':
            current_node = current_node.childR
        sum += current_node.value

    return sum
"""

def treesum_2(entrylist, route):
    sum = 0
    while True:
        listmiddle = ceil(len(entrylist)/2)-1
        sum += entrylist[listmiddle]
        if route == "":
            break
        elif route[0] == "L":
            entrylist = entrylist[:listmiddle]
        elif route[0] == "R":
            entrylist = entrylist[listmiddle+1:]
        route = route[1:]
    return sum


entrylist = [int(x) for x in input().split()]
route = input()
print(treesum_2(entrylist,route))
"""
testroute = "LRLRLRLRLRLRLRLRLRLRL"
testlist = [6 for i in range(2**22-1)]
pr.run("print(treesum_2(testlist, testroute))")
"""