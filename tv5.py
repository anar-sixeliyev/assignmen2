from queue import Queue
import sys
sys.setrecursionlimit(10000)  # Increase the recursion limit to 10,000

def revise(csp, Xi, Xj):
    print(f"===> Before: {Xi}: {csp[Xi]}, {Xj}: {csp[Xj]}")

    revised = False
    for x in csp[Xi]:
        if not any(csp[Xj][k] != y for k, y in enumerate(csp[Xi]) if k != x):
            csp[Xi].remove(x)
            revised = True
    print(f"===> After: {Xi}: {csp[Xi]}, {Xj}: {csp[Xj]}\n")

    return revised

def AC3(csp, queue=None):
    if queue is None:
        queue = Queue()
        for Xi in csp:
            for Xj in csp:
                if Xj != Xi:
                    queue.put((Xi, Xj))

    while not queue.empty():
        (Xi, Xj) = queue.get()
        if revise(csp, Xi, Xj):
            if len(csp[Xi]) == 0:
                return False
            for Xk in csp:
                if Xk != Xi and Xk != Xj:
                    queue.put((Xk, Xi))
    return True

# def graph_coloring(csp, colors):
#     AC3(csp)
#     if all(len(csp[var]) == 1 for var in csp):
#         return {var: csp[var][0] for var in csp}
#     var = min(csp, key=lambda x: len(csp[x])) # Choose variable with minimum remaining values
#     for color in colors:
#         if all(color != csp[neighbor][0] for neighbor in csp[var]):
#             csp_copy = {key: value[:] for key, value in csp.items()}
#             csp_copy[var] = [color]
#             result = graph_coloring(csp_copy, colors)
#             if result is not None:
#                 return result
#     return None
def graph_coloring(csp, colors):
    AC3(csp)
    if all(len(csp[var]) == 1 for var in csp):
        return {var: csp[var][0] for var in csp}
    var = min(csp, key=lambda x: len(csp[x])) # Choose variable with minimum remaining values
    for color in range(1, colors+1):
        if all(color != csp[neighbor][0] for neighbor in csp[var]):
            csp_copy = {key: value[:] for key, value in csp.items()}
            csp_copy[var] = [color]
            result = graph_coloring(csp_copy, colors)
            if result is not None:
                return result
    return None

graph = {
    1: {3},
    2: {18, 19},
    3: {1, 19},
    18: {2},
    19: {2, 3}
}
# csp = {var: [0, 1, 2] for var in graph}
colors =3
csp = {var: list(range(1, colors+1)) for var in graph}

# colors = ['red', 'green', 'blue']


AC3(csp)
# solution = graph_coloring(csp, colors)
# print(solution)
