import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMapA = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getAllCategories(self):
        return DAO.getAllCategories()

    def creaGrafo(self, nomeC, anno1, anno2):
        self._grafo.clear()
        self._idMapA.clear()

        prodotti = DAO.getAllNodes(nomeC)
        for a in  prodotti:
            self._idMapA[a.product_id] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in prodotti:
            # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a.list_prodotti = DAO.getProdottiPerPeriodo(a.product_id, anno1, anno2)
            # a.popolarita = DAO.getPopolarita(a.ArtistId)
            a.num_vendite = len(a.list_prodotti)
        print("3 - Informazioni recuperate")

        for i in range(len(prodotti)):
            a1 = prodotti[i]
            for j in range(i + 1, len(prodotti)):
                a2 = prodotti[j]

                n1 = a1.num_vendite
                n2 = a2.num_vendite

                if n1 > 0 and n2 > 0:
                    peso = n1 + n2

                #prodotti_Comuni = (set(a1.list_prodotti) & set(a2.list_prodotti))
                # ND: & FUNZIONA SOLO CON I SET! SE HAI LE LISTE CONSERVTILE IN SET E POI CONFRONTALE
               # if len(prodotti_Comuni) > 0:
                   # peso = len(prodotti_Comuni)
                   # p1=len(a1.list_prodotti)
                    #p2 = len(a2.list_prodotti)
                    if n1 > n2:
                        self._grafo.add_edge(a1, a2, weight=peso)

                    elif n2 > n1:
                        self._grafo.add_edge(a2, a1, weight=peso)
                    else:
                        self._grafo.add_edge(a1, a2, weight=peso)
                        self._grafo.add_edge(a2, a1, weight=peso)
        print("4 - Archi aggiunti")

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getAllNodes(self, nomeC):
        return DAO.getAllNodes(nomeC)

    def get5ProdottiPiuVenduti(self):
        risultati = []

        for p in self._grafo.nodes:
            uscenti = self._grafo.out_edges(p, data=True)
            entranti = self._grafo.in_edges(p, data=True)

            valore = sum(d["weight"] for _, _, d in uscenti) - \
                     sum(d["weight"] for _, _, d in entranti)

            risultati.append((p, valore))

        risultati.sort(key=lambda x: x[1], reverse=True)

        return risultati[:5]

    def getProdottoByNome(self, nome):
        for p in self._grafo.nodes:
            if f"{p.product_name} - {p.model_year}" == nome:
                return p
        return None



    def getGruppoProdotti(self,  k, start_node,end_node):
        self._best_path = []
        self._best_score = float("-inf")

       # self._creaMappaComponenti()
        #prodotti= list(self._grafo.nodes)

        # Il percorso parziale parte con il nodo selezionato
        parziale = [start_node]
        self._ricorsione(parziale, k, end_node, 0)

        return self._best_path, self._best_score

    def _ricorsione(self, parziale, k, end_node, score):
        ultimo = parziale[-1]
        # Caso terminale: abbiamo raggiunto la lunghezza richiesta
        if len(parziale) == k:
            if ultimo == end_node:
               # score = sum(len(a.num_vendite) for a in parziale)
                if score > self._best_score:
                    self._best_score = score
                    self._best_group = list(parziale)
                return
        # Se arriviamo alla destinazione troppo presto, ci fermiamo
        if parziale[-1]==end_node:
            return

       # candidati = set()

        # Provo tutti i nodi raggiungibili dall'ultimo nodo
        for vicino in self._grafo.successors(ultimo):

            # Un nodo non può essere visitato più volte
            if vicino not in parziale:
                peso = self._grafo[ultimo][vicino]["weight"]

        # RACCOLGO I REGISTI ADIACENTI
       # for p in parziale:
          #  candidati.update(self._grafo.neighbors(p))
        # provo solo i candidati adiacenti a qualcuno del gruppo
       # for candidato in candidati:
         #   if candidato in parziale:
              #  continue
            # Il candidato non deve essere collegato con peso 1 a nessun artista già selezionato
           # valido = True
          #  for prod in parziale:
              #  if self._grafo.has_edge(prod, candidato):
                   # peso = self._grafo[prod][candidato].get("weight")

                new_score=score+peso
                parziale.append(vicino)
                # Chiamata ricorsiva passando il nuovo arco come riferimento
                self._ricorsione(parziale, k,end_node, new_score)
                # BACKTRACKING: annullo l'ultima mossa
                parziale.pop()




