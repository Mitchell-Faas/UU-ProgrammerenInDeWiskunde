
def lees_invoer():
    graph = {}
    n = int(input())
    for i in range(n):
        v = input().split()
        graph[v[0]] = v[1:]
    return graph

graph = lees_invoer()
start, finish = input().split()

path_queue = [[start]]

target_reached = False
while not target_reached:
    current_path = path_queue.pop()
    for node in graph[str(current_path[-1])]:
        new_path = current_path.copy()
        new_path.append(node)
        if node == finish:
            target_reached = True
            path_to_target = new_path
        path_queue.insert(0,new_path)

print(len(path_to_target)-1)
