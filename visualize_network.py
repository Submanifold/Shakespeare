#!/usr/bin/env python3
#
# Visualizes a given Pajek graph using a spring-based algorithm and
# writes the result to STDOUT. The output format follows the syntax
# of the 'TikZ' package [1], meaning that the output can be readily
# included in LaTeX documents.
#
# [1]: https://sourceforge.net/projects/pgf/

import networkx as nx
import sys

filename  = sys.argv[1]
G         = nx.read_pajek(filename)
positions = nx.drawing.nx_agraph.graphviz_layout(G, prog='neato')
threshold = float('inf') if len(sys.argv) <= 2 else float(sys.argv[2])

name_to_index = dict()
for index,name in enumerate(sorted(positions.keys())):
    name_to_index[name] = index

min_pos =  1e6
max_pos = -1e6

for name in positions.keys():
    x,y = positions[name]
    min_pos = min(min_pos, min(x,y))
    max_pos = max(max_pos, max(x,y))

print("\\begin{tikzpicture}")
for name in sorted(positions.keys()):
    i   = name_to_index[name]
    x,y = positions[name]

    x = 5*(x - min_pos) / (max_pos - min_pos)
    y = 5*(y - min_pos) / (max_pos - min_pos)

    print("  \\node (%03d) at (%3.2f,%3.2f) {};" % (i,x,y))

minData =  1e6
maxData = -1e6

for edge in G.edges(data=True):
    _, _, data = edge
    minData = min(minData, data['weight'])
    maxData = max(maxData, data['weight'])

for edge in G.edges(data=True):
    source, target, data = edge

    u = name_to_index[source]
    v = name_to_index[target]
    w = data['weight']

    if w <= threshold:
        w = (w - minData)  / (maxData - minData)
        w = w * 2 + 0.10

        print("  \\draw[line width=%.2fmm] (%03d.center) edge (%03d.center);" % (w,u,v))

for name in sorted(positions.keys()):
    i = name_to_index[name]
    print("  \\filldraw[cardinal] (%03d) circle (1pt);" % (i))

print("\\end{tikzpicture}")
