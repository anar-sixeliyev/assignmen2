from queue import Queue
# from collections import deque

class GraphColoringCSP:
    
    def __init__(self, graph, num_colors):
        self.graph = graph
        self.num_colors = num_colors
    
    def AC3(self, queue=None):
        if queue is None:
            queue = Queue()
            for Xi in self.graph:
                for Xj in self.graph:
                    if Xj != Xi:
                        queue.put((Xi, Xj))
        # if queue is None:
        #     queue = deque((i, j) for i in self.graph for j in self.graph[i])

        while not queue.empty():
            (Xi, Xj) = queue.get()
            if self.revise(Xi, Xj):
                if len(csp[Xi]) == 0:
                    return False
                for Xk in csp:
                    if Xk != Xi and Xk != Xj:
                        queue.put((Xk, Xi))
        return True

    def revise(self, Xi, Xj):
        revised = False
        print(f"===> Before: {Xi}: {self.domain[Xi]}, {Xj}: {self.domain[Xj]}")

        for x in self.graph[Xi]:
            if not any(self.graph[Xj][k] != y for k, y in enumerate(self.graph[Xi]) if k != x):
                self.domain[Xi].remove(x)
                revised = True
        print(f"===> After: {Xi}: {self.domain[Xi]}, {Xj}: {self.domain[Xj]}")
        
        return revised

    def solve(self):
        self.domain = {v: set(range(self.num_colors)) for v in self.graph}
        print('domain before', self.graph)
        self.AC3()

# create a graph
graph = {
    1: {3},
    2: {18, 19},
    3: {1, 19},
    18: {2},
    19: {2, 3}
}
colors =3

csp = GraphColoringCSP(graph, num_colors=colors)

color_map = csp.solve()

