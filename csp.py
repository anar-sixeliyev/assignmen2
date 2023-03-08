from collections import deque

class GraphColoringCSP:
    
    def __init__(self, graph, num_colors):
        self.graph = graph
        self.num_colors = num_colors
        
    def is_valid_color(self, vertex, color, color_map):
        for neighbor in self.graph[vertex]:
            if color_map.get(neighbor) == color:
                return False
        return True
    
    def get_unassigned_var(self, color_map):
        for vertex in self.graph:
            if vertex not in color_map:
                return vertex
        return None
    
    def get_ordered_domain_values(self, var, color_map):
        domain = set(range(self.num_colors))
        for neighbor in self.graph[var]:
            if neighbor in color_map:
                domain.discard(color_map[neighbor])
        return sorted(domain, key=lambda c: self.count_conflicts(var, c, color_map))
    
    def count_conflicts(self, var, color, color_map):
        conflicts = 0
        for neighbor in self.graph[var]:
            if neighbor in color_map and color_map[neighbor] == color:
                conflicts += 1
        return conflicts
    
    def ac3(self, queue=None):
        if queue is None:
            queue = deque((i, j) for i in self.graph for j in self.graph[i])
        while queue:
            i, j = queue.popleft()
            if self.revise(i, j):
                if not self.graph[i]:
                    return False
                for k in self.graph[i]:
                    if k != j:
                        queue.append((k, i))
        return True
    
    def revise(self, i, j):
        revised = False
        for ci in list(self.domain[i].copy()):
            if not any(self.is_valid_color(j, cj, {i: ci}) for cj in self.domain[j]):
                self.domain[i].remove(ci)
                revised = True
        return revised
    
    def backtrack(self, color_map):
        if len(color_map) == len(self.graph):
            return color_map
        var = self.get_unassigned_var(color_map)
        for value in self.get_ordered_domain_values(var, color_map):
            if self.is_valid_color(var, value, color_map):
                color_map[var] = value
                inferences = self.inference(var, value, color_map)
                if inferences is not None:
                    result = self.backtrack(color_map)
                    if result is not None:
                        return result
                del color_map[var]
                self.restore_domain(inferences)
        return None
    
    def inference(self, var, value, color_map):
        inferences = []
        for neighbor in self.graph[var]:
            if neighbor not in color_map:
                for color in self.domain[neighbor].copy():
                    if not self.is_valid_color(neighbor, color, {var: value, neighbor: color}):
                        self.domain[neighbor].remove(color)
                        inferences.append((neighbor, color))
                if not self.domain[neighbor]:
                    return None
        return inferences
    
    def restore_domain(self, inferences):
        for var, value in inferences:
            self.domain[var].add(value)
            
    def solve(self):
        self.domain = {v: set(range(self.num_colors)) for v in self.graph}
        print(self.domain)
        self.ac3()
        color_map = self.backtrack({})
        return color_map

# create a graph
graph = {
    1: {3},
    2: {18, 19},
    3: {1, 19},
    18: {2},
    19: {2, 3}
}

# create a CSP solver
csp = GraphColoringCSP(graph, num_colors=3)

# solve the problem
color_map = csp.solve()

# print the result
for vertex, color in color_map.items():
    print(f"Vertex {vertex} is assigned color {color}")
