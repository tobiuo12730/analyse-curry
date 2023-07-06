#%%
import xml.etree.ElementTree as ET
from rapidfuzz import fuzz
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def describe(node,nodes):
    node = nodes.findall(f"./Node[@Name='{node.attrib['Name']}']")[0]
    return f'{"@".join([f"{node.attrib[key]}" for key in sorted(node.attrib.keys())])}'

def describe_all(input, node, output, nodes):
    return "(" + ",".join([describe(x, nodes) for x in input]) + ")>"+describe(node, nodes)+">(" + ",".join([describe(x, nodes) for x in output]) + ")"

def describe_file(file):
    tree = ET.parse(file)
    root = tree.getroot()

    nodes = root.findall("./Nodes")[0]
    edges = root.findall("./Edges")[0]

    txts = []
    for node in nodes.findall("./Node"):
        input = edges.findall(f"./Edge/To/Node[@Name='{node.attrib['Name']}']/../../From/Node")
        output = edges.findall(f"./Edge/From/Node[@Name='{node.attrib['Name']}']/../../To/Node")

        txts.append(describe_all(input,node,output,nodes))

    return nodes, edges, txts

na, ea, ta = describe_file("a.xml")
nb, eb, tb = describe_file("b.xml")

r = np.array([[fuzz.ratio(a, b) for a in ta] for b in tb])

ordb = []
for row in r:
    arg = np.argmax(row)
    ordb.append(arg)
    r[:,arg]=0


with open("b2.xml", "wb") as f:
    for idx in ordb:
        f.write(ET.tostring(nb[ordb[idx]]))

