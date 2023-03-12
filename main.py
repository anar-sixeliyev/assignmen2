import sys
from collections import deque
sys.setrecursionlimit(10**6)
from queue import PriorityQueue

class GraphColoringCSP:
    
    def __init__(self, graph, num_colors):
        self.graph = graph
        self.num_colors = num_colors
        self.domain = {v: set(range(self.num_colors)) for v in self.graph}
        self.checkValid()
        
    def checkValid(self):
        for node,nexts in self.graph.items():
            if node in nexts:
                raise ValueError(f"Node {node} is linked to itself.")
            for next in nexts:
                if next not in self.graph or node not in self.graph[next]:
                    raise ValueError(f"Node {node} is not properly linked to node {next}.")

    def MRVgetUnassignedArea(self, color_map):
        unassigned = PriorityQueue()
        for v in self.graph:
            if v not in color_map:
                unassigned.put((len(self.domain[v]), v))
        return unassigned.get()[1]

    def LCVgetOrderedDomainValues(self, node, color_map):
        domain = self.domain[node]
        if len(domain) == 1:
            return domain
        conflicts = [(c, self.countConflicts(node, c, color_map)) for c in domain]
        conflicts.sort(key=lambda x: x[1])
        return [c[0] for c in conflicts]

    def countConflicts(self, node, color, color_map):
        conflicts = 0
        for neighbor in self.graph[node]:
            if neighbor in color_map and color_map[neighbor] == color:
                conflicts += 1
        return conflicts
    
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
    
    def removeInconsistentValues(self, i, j):
        removed = False
        for ci in list(self.domain[i].copy()):
            if not any(self.isValidColor(j, cj, {i: ci}) for cj in self.domain[j]):
                self.domain[i].remove(ci)
                removed = True
        return removed
    
    def isValidColor(self, vertex, color, color_map):
        for neighbor in self.graph[vertex]:
            if color_map.get(neighbor) == color:
                return False
        return True

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

    def undoForwardChecking(self, inferences):
        if(inferences):
            for var, value in inferences:
                self.domain[var].add(value)


    def forwardChecking(self, node, value, color_map):
        inferences = []
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
        for vertex, color in sorted(color_map.items()):
            print(f"Vertex {vertex} is assigned color {color}")
    else:
        print('\tIt is not possible to color this Graph')

processFile()
