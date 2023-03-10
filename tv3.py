# def AC3(csp, queue=None, domains=None):
#     if queue is None:
#         queue = [(i, j) for i in csp.variables for j in csp.neighbors[i]]
#     if domains is None:
#         domains = {v: set(csp.domains[v]) for v in csp.variables}
#     while queue:
#         (xi, xj) = queue.pop(0)
#         if revise(csp, xi, xj, domains):
#             if not domains[xi]:
#                 return False
#             for xk in csp.neighbors[xi]:
#                 if xk != xj:
#                     queue.append((xk, xi))
#     return True
def AC3(csp, queue, domains):
    while queue:
        (xi, xj) = queue.pop(0)
        revised = False
        for x in domains[xi].copy():
            if not any(csp.constraints(xi, x, xj, y) for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        if revised:
            if len(domains[xi]) == 0:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj, domains):
    revised = False
    for x in domains[xi]:
        if not any([csp.constraints(xi, x, xj, y) for y in domains[xj]]):
            domains[xi].remove(x)
            revised = True
    return revised

from typing import List, Tuple
from collections import defaultdict

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

def graph_coloring(num_nodes: int, edges: List[Tuple[int,int]], num_colors: int) -> List[int]:
    variables = list(range(num_nodes))
    domains = {v: set(range(num_colors)) for v in variables}
    neighbors = defaultdict(set)
    for i, j in edges:
        neighbors[i].add(j)
        neighbors[j].add(i)
    def constraints(xi, x, xj, y):
        return x != y and (xi, xj) in edges
    csp = CSP(variables, domains, neighbors, constraints)
    while domains:
        variable = min(domains, key=lambda v: len(domains[v]))
        if not domains[variable]:
            return None
        value = domains[variable].pop()
        if AC3(csp, [(variable, neighbor) for neighbor in neighbors[variable]], domains):
            if not domains:
                return None
        else:
            domains[variable].add(value)
    return [domains[i].pop() for i in range(num_nodes)]



# Example graph
num_nodes = 5
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
num_colors = 3

# Solve the graph coloring problem
colors = graph_coloring(num_nodes, edges, num_colors)

# Print the results
print(f"Colors for each node: {colors}")
