from collections import deque
# Input function from hint.
def read_input():
    graph = {}
    n = int(input())
    for i in range(n):
        v = input().split()
        graph[v[0]] = v[1:]
    return graph

# Get the graph
graph = read_input()

# Get the goal
start, finish = input().split()

# Use a breadth first search
paths = deque()
path = [start]
paths.append(path)
visited_nodes = [start]
# If we found the one, end.
while path[-1] != finish:
    try:
        path = paths.popleft()
    except IndexError:
        # No paths left
        print(-1)
        break

    # For each connection
    for connected_node in graph[path[-1]]:
        # If the connection has not already been reached
        if connected_node not in visited_nodes:
            # Add to search queue
            new_path = path.copy()
            new_path.append(connected_node)
            paths.append(new_path)

            # Add to visited nodes
            visited_nodes.append(connected_node)
else:
    # The while condition failed, so we're at the finish.
    print(len(path)-1) # Subtract one to account for the start