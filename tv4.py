from queue import Queue

def graph_coloring_AC3(graph, domains):
    """Solves the graph coloring problem using AC3 algorithm with constraint propagation.

    Parameters:
    graph (dict): A dictionary representing the graph where each key is a node and the values are a list of its neighbors.
    domains (dict): A dictionary where each key is a node and the value is a list of possible colors for that node.

    Returns:
    A dictionary representing the final assignment of colors where each key is a node and the value is its assigned color.
    If there is no valid coloring, returns None.
    """
    # Initialize the queue with all the arcs in the graph
    queue = Queue()
    for node in graph:
        for neighbor in graph[node]:
            queue.put((node, neighbor))

    # Loop while there are still arcs to process
    while not queue.empty():
        (i, j) = queue.get()
        revised = False

        # Check for arc consistency between i and j
        for color_i in domains[i]:
            if not any([color_i != color_j for color_j in domains[j]]):
                domains[i].remove(color_i)
                revised = True

        if revised:
            if len(domains[i]) == 0:
                return None
            # Add all the arcs pointing to i, except the current one, to the queue
            for neighbor in graph[i]:
                if neighbor != j:
                    queue.put((neighbor, i))

    # If we get here, the domains are arc-consistent
    # Assign colors to the nodes
    assignment = {}
    for node in domains:
        if len(domains[node]) == 1:
            assignment[node] = domains[node][0]
        else:
            return None

    return assignment


# Sample graph and domains
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['B', 'C', 'E', 'F'],
    'E': ['C', 'D', 'F'],
    'F': ['D', 'E']
}
domains = {
    'A': ['red', 'green', 'blue'],
    'B': ['red', 'green'],
    'C': ['blue'],
    'D': ['red', 'green'],
    'E': ['red', 'green', 'blue'],
    'F': ['red', 'green', 'blue']
}

# Call the function to solve the graph coloring problem
result = graph_coloring_AC3(graph, domains)

# Print the final result
if result:
    print("Final assignment of colors:")
    for node in result:
        print(node + ": " + result[node])
else:
    print("No valid coloring found.")
