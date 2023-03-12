import sys
from collections import deque
sys.setrecursionlimit(10**6)
from queue import PriorityQueue

class GraphColoringCSP:

    # initialize the graph with properties and checking validity
    def __init__(self, graph, num_colors):
        self.graph = graph
        self.num_colors = num_colors
        self.domain = {v: set(range(self.num_colors)) for v in self.graph}
        self.checkValid()

    # check if the graph is valid or not
    def checkValid(self):
        for node,nexts in self.graph.items():
            if node in nexts:
                raise ValueError(f"Node {node} is linked to itself.")
            for next in nexts:
                if next not in self.graph or node not in self.graph[next]:
                    raise ValueError(f"Node {node} is not properly linked to node {next}.")

    # MRV: get the node with minimum remaining values
    def MRVgetUnassignedArea(self, color_map):
        unassigned = PriorityQueue()
        for v in self.graph:
            if v not in color_map:
                unassigned.put((len(self.domain[v]), v))
        return unassigned.get()[1]

    # LCV: get the ordered domain values using least constraining value heuristic
    def LCVgetOrderedDomainValues(self, node, color_map):
        domain = self.domain[node]
        if len(domain) == 1:
            return domain
        conflicts = [(c, self.countConflicts(node, c, color_map)) for c in domain]
        conflicts.sort(key=lambda x: x[1])
        return [c[0] for c in conflicts]
    
    # count the conflicts between the given node and its neighbors
    def countConflicts(self, node, color, color_map):
        conflicts = 0
        for neighbor in self.graph[node]:
            if neighbor in color_map and color_map[neighbor] == color:
                conflicts += 1
        return conflicts
    
    # arc consistency
    def AC_3(self, queue=None):
        if queue is None:
            queue = deque((i, j) for i in self.graph for j in self.graph[i])
        while queue:
            i, j = queue.popleft()
            if self.removeInconsistentValues(i, j):
                if not self.domain[i]:
                    return False
                for k in self.graph[i]:
                    if k != j:
                        queue.append((k, i))
        return True
    
    # remove inconsistent values from the domain of a variable
    def removeInconsistentValues(self, i, j):
        removed = False
        for ci in list(self.domain[i].copy()):
            if not any(self.isValidColor(j, cj, {i: ci}) for cj in self.domain[j]):
                self.domain[i].remove(ci)
                removed = True
        return removed
    
    # check if a color is valid for a vertex or not
    def isValidColor(self, vertex, color, color_map):
        for neighbor in self.graph[vertex]:
            if color_map.get(neighbor) == color:
                return False
        return True

    # implement backtrack search algorithm
    def backtrack(self, color_map):
        if len(color_map) == len(self.graph):
            return color_map
        
        node = self.MRVgetUnassignedArea(color_map)
        ordered_values = self.LCVgetOrderedDomainValues(node, color_map)
        
        for value in ordered_values:
            if self.isValidColor(node, value, color_map):
                color_map[node] = value
                
                inferences = self.forwardChecking(node, value, color_map)
                if inferences is not None:
                    result = self.backtrack(color_map)
                    if result is not None:
                        return result
                    
                del color_map[node]
                self.undoForwardChecking(inferences)
                
        return None

    #  restore the removed values to the domains of affected nodes
    def undoForwardChecking(self, inferences):
        if(inferences):
            for var, value in inferences:
                self.domain[var].add(value)

    def forwardChecking(self, node, value, color_map):
        inferences = []
        # Check each neighbor of the node and removes the value from its domain if it is not consistent with the color assignment of the node.
        for neighbor in self.graph[node]:
            if neighbor not in color_map:
                if value in self.domain[neighbor]:
                    self.domain[neighbor].remove(value)
                    inferences.append((neighbor, value))
                if not self.domain[neighbor]:
                    return None
        return inferences
    
    
    def solve(self):
        self.AC_3()
        color_map = self.backtrack({})
        return color_map

#  read a graph from a file and return it as dictionary
def read_graph(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            if line.startswith('colors') or line.startswith('Colors') :
                colors = int(line.split('=')[1].strip())
                continue
            edge = tuple(sorted(map(int, line.split(','))))
            graph.setdefault(edge[0], set()).add(edge[1])
            graph.setdefault(edge[1], set()).add(edge[0])
    return graph, colors


def processFile():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        return

    graph, num_colors = read_graph(sys.argv[1])
    csp = GraphColoringCSP(graph, num_colors)
    color_map = csp.solve()
    if(color_map):
        # For readability, sort the color_map before printing because it could be not in inreasing order
        for vertex, color in sorted(color_map.items()):
            print(f"Vertex {vertex} is assigned color {color}")
    else:
        print('\tIt is not possible to color this Graph')

processFile()
