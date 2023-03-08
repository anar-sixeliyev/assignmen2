import sys
# read file name and seperate to graph and colors
def read_graph(file_name):
    graph = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            if line.startswith('colors') or line.startswith('Colors') :
                print(line)
                colors = int(line.split('=')[1].strip())
                continue
            edge = tuple(sorted(map(int, line.split(','))))
            graph.setdefault(edge[0], set()).add(edge[1])
            graph.setdefault(edge[1], set()).add(edge[0])
    return graph, colors

def is_valid_color(graph, vertex, color, color_map):
    for neighbor in graph[vertex]:
        if color_map.get(neighbor) == color:
            return False
    return True

def get_color_for_vertex(graph, vertex, color_map, num_colors):
    for color in range(num_colors):
        if is_valid_color(graph, vertex, color, color_map):
            return color
    return None

def color_graph(graph, num_colors):
    color_map = {}
    for vertex in sorted(graph.keys()):
        color = get_color_for_vertex(graph, vertex, color_map, num_colors)
        if color is None:
            raise ValueError('Failed to color graph')
        color_map[vertex] = color
    return color_map

def processFile():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        return

    graph, num_colors = read_graph(sys.argv[1])
    print('num_colors', num_colors)
    print('graph', graph)

    color_map = color_graph(graph, num_colors)
    print('color_map', color_map)

processFile()