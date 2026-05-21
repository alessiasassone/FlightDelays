#Creo questo test per vedere se i nodi creati sono in numero ragionevole
#Creo istanza modello
from model.model import Model

myModel = Model()
myModel.buildGraph(5)
nNodes, nEdges = myModel.getGraphDetails()
# print(f"Num nodes: {nNodes}, num edges: {nEdges}")