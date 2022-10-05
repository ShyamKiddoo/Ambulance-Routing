import sys
from heapq import heapify, heappush, heappop
from pyvis.network import Network


class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, elem):
        if elem not in self.adj_list:
            self.adj_list[elem] = {}

    def add_edge(self, src, dest, weight):
        if src in self.adj_list:
            self.adj_list[src] = self.adj_list[src] | {dest: weight}

    def display(self):
        print(self.adj_list)


def dijsktra(graph, src, dest):
    inf = sys.maxsize
    node_data = {}

    for node in graph:
        node_data = node_data | {node: {"cost": inf, "pred": []}}

    node_data[src]["cost"] = 0
    visited = []
    temp = src

    for i in range(len(graph)-1):

        if temp not in visited:
            visited.append(temp)
            min_heap = []

            for j in graph[temp]:

                if j not in visited:
                    cost = node_data[temp]["cost"] + graph[temp][j]

                    if cost < node_data[j]["cost"]:
                        node_data[j]["cost"] = cost
                        node_data[j]["pred"] = node_data[temp]["pred"] + [temp]
                    heappush(min_heap, (node_data[j]["cost"], j))

        heapify(min_heap)
        if min_heap == []:
            break
        temp = min_heap[0][1]

    cost_of_path = node_data[dest]["cost"]
    optimal_path = node_data[dest]["pred"] + [dest]
    print("Shortest Distance:", cost_of_path)
    print("Stortest Path:", optimal_path)

    return cost_of_path, optimal_path


def display_graph_network(path, g):

    net = Network("100vh", "100%", directed=True)

    for i, node in enumerate(g.adj_list):

        if node.startswith("az-"):
            net.add_node(node, title="Accident Zone " + node, color="brown", size=22)

        elif node.startswith("mh-"):
            net.add_node(node, title="Multispeciality Hospital " + node, color="green", size=25)

        elif node.startswith("h-"):
            net.add_node(node, title="Hospital " + node, size=18)

    for node in g.adj_list:
        for j in g.adj_list[node]:

            if node == path[0] and j == path[1]:
                net.add_edge(node, j, label=str(g.adj_list[node][j]), color="red")
                path.pop(0)

            else:
                net.add_edge(node, j, label=str(g.adj_list[node][j]), color="#000000")
    net.show("graph.html")


g = Graph()

f = open("graph_input.txt", 'r')
lines = f.readlines()

for line in lines:
    
    line = line.strip('\n')
    if line == "":
        break
    line = line.split()
    if len(line) == 1:
            g.add_node(line[0])
    elif len(line) == 3:
            g.add_edge(line[0], line[1], int(line[2]))

house_start = input("Enter the accident zone:")

min_cost = sys.maxsize
min_path = []
min_hospt = ""
hospitals = list(filter(lambda x: x.startswith("mh-"), list(g.adj_list.keys())))

for hospt in hospitals:
    cost, path = dijsktra(g.adj_list, house_start, hospt)

    if cost < min_cost:
        min_cost = cost
        min_path = path
        min_hospt = hospt

path = min_path.copy()
display_graph_network(min_path, g)

import bs4

with open("graph.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt, features="html.parser")


tailwind_script = soup.new_tag("script", src="https://cdn.tailwindcss.com")

soup.head.append(tailwind_script)
box = soup.new_tag(
    "div",
    attrs={
        "class": "w-96 shadow-lg z-10 absolute top-5 right-5 bg-gray-200 border-2 border-gray-300 rounded-lg p-4"
    },
)
heading = soup.new_tag("h1", attrs={"class": "text-xl font-bold text-gray-700"})
heading.string = "Ambulance Routing System"

box.append(heading)


p_tag1 = bs4.BeautifulSoup(
    f'<p class="mt-4 text-gray-600"><span class="font-bold">(Source): </span> {house_start}</p>',
    features="html.parser",
)

p_tag2 = bs4.BeautifulSoup(
    f'<p class="mt-1 text-gray-600"><span class="font-bold">Nearest Multi-Speciality Hospital (Dest.):  </span> {min_hospt}</p>',
    features="html.parser",
)

p_tag3 = bs4.BeautifulSoup(
    f'<p class="mt-1 text-gray-600"><span class="font-bold">Shortest Path Length: </span> {min_cost}</p>',
    features="html.parser",
)

p_tag4 = bs4.BeautifulSoup(
    f'<p class="mt-1 text-gray-600"><span class="font-bold">Shortest Path:  </span> {", ".join(path)}</p>',
    features="html.parser",
)

p_tag5 = bs4.BeautifulSoup(
    f'<p class="mt-4 text-gray-800"><span class="font-bold">Project By: </span> Sai Shyam & Sai Shanmat </p>',
    features="html.parser",
)

p_tag6 = bs4.BeautifulSoup(
    f'<p class="mt-4 text-gray-700">The Multi-Speciality Hospital is denoted by <span class="text-green-600 font-bold">Green</span> colour and the Accident Zones are denoted by <span class="text-red-600 font-bold">Brown</span> colour. The Hospitals are denoted by <span class="text-blue-300 font-bold">Blue</span> colour And the shortest path edges are highlighted in <span class="text-red-500 font-bold">Red</span> color.</p>',
    features="html.parser",
)

box.append(p_tag1)
box.append(p_tag2)
box.append(p_tag3)
box.append(p_tag4)
box.append(p_tag6)
box.append(p_tag5)

soup.body.append(box)

with open("graph.html", "w") as outf:
    outf.write(str(soup))
