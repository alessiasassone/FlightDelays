import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        # Creo un grafo, semplice
        self._graph = nx.Graph()
        #creo un parametro airports che riempio con il metodo del DAO --> ho tutti gli aeroporti
        self._airports = DAO.getAllAirports()
        # Mappa che recupera l'aeroporto a partire da un intero, cioè la sua chiave primaria
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino = []
        self._bestScore = 0

        parziale = [v0]

        self._ricorsione(parziale, v1, t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        # Verifico se parziale è una soluzione valida ed in caso la salvo
        if parziale[-1] == v1: # potenzialmente questa è una sol accettabile
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
        # Verifico se ha senso continuare ad aggiungere elementi in parziale
        if len(parziale) == t+1: #Allora parziale ha già raggiunto il numero massimo di tratte
            return
        # espando parzila e faccio ricorsione con backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def _getScore(self, parziale):
        sumPesi = 0
        for i in range (0,len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]['weight']
        return sumPesi

    def buildGraph(self, nMin):
        # Recupera nodi
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self._graph.clear_edges()
        self.addEdgesV2()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")

    def addEdges(self):
        # Queste tratte hanno 2 problemi:
        # 1) ho archi diretti e inversi e quindi dovrò fare la somma a mano
        # 2) ho archi fra aeroporti che avevo filtrato
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)

        # Se c'è un problema nel calcolo degli archi si nota perchè cambia il numero di nodi
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getViciniOrdinati(self, source):
        # Restituisce tutti i vicini di source ordinati per peso dell'arco che collega source al vicino
        vicini = self._graph.neighbors(source)
        viciniT = []
        for v in vicini:
            viciniT.append( (v, self._graph[source][v]['weight']) )
        viciniT.sort(key=lambda x: x[1], reverse=True) # vedo il valore in posizione 1 (peso) e lo ordino
        return viciniT

    def hasPath(self, v0, v1):
        # Restituisce true se un qualche cammino fra v0 e v1 esiste, false altrimenti
        return v1 in nx.node_connected_component(self._graph, v0) #componente connesa che contiene v0 e ppi verifichiamo se v1 è presente

    def getPath(self, v0, v1):
        # Diversi modi per implementare:
        # v1
        # dictOfPredecessors = dict( nx.bfs_predecessors(self._graph, v0) ) # ogni nodo sarà una chiave, e per ognuno mi dice qual è il nodo precedente nell'albero di visita
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, dictOfPredecessors[path[0]]) # path = [v0, -----, v1]
        #
        # v2
        # dictOfPredecessors = dict(nx.dfs_predecessors(self._graph, v0))
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, dictOfPredecessors[path[0]])
        #
        # v3
        # path = nx.shortest_path(v0, v1)

        # v4: forse questo è il più immediato, gli sto dicendo di cercare il cammino minimo senza badare al peso
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)
        return path

    def getGraphDetails(self):
        # Fa una return di numero nodi e num archi contati
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes
