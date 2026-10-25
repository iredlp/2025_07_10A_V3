import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCategory(self):
        try:
            category = self._model.getAllCategories()
            for y in  category:
                self._view._ddcategory.options.append(ft.dropdown.Option(y))
                # key=actor.id,
                #  text=actor.name))
           # self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero della categoria: {ex}", color="red"))
        self._view.update_page()

    def fillDDNodoStart(self, categoria):
        try:
            prodotti = self._model.getAllNodes(categoria)
            for p in prodotti:
                self._view._ddProdStart.options.append(ft.dropdown.Option( key=str(p.product_id),
                                                         text=f"{p.product_name} - {p.model_year}"))
                # key=actor.id,
                #  text=actor.name))
             #self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero della categoria: {ex}", color="red"))
        self._view.update_page()

    def fillDDNodoEnd(self, categoria):
        try:
            prodotti = self._model.getAllNodes(categoria)
            for p  in prodotti:
                self._view._ddProdEnd.options.append(ft.dropdown.Option( key=str(p.product_id),
                                text=f"{p.product_name} - {p.model_year}"))
                # key=actor.id,
                #  text=actor.name))
            self._view.update_page()

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore nel recupero della categoria: {ex}", color="red"))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        anno1 = self._view._dp1.value
        anno2 = self._view._dp2.value
        categoria = self._view._ddcategory.value
        if not anno1:
            self._view.create_alert("Selezionare la prima data prima di creare il grafo.", color="red")
            return
        if not anno2:
            self._view.create_alert("Selezionare la seconda data prima di creare il grafo.", color="red")
            return
        if not categoria:
            self._view.create_alert("Selezionare la CATEGORIA prima di creare il grafo.", color="red")
            return

        try:
            self._model.creaGrafo(categoria,anno1, anno2)
            self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno1}", color="green"))
            self._view._txt_result.controls.append(ft.Text(f"Data selezionata: {anno2}\n", color="green"))
            n_nodes = self._model.get_num_nodes()
            n_edges = self._model.get_num_edges()
            # Stampa immediata numero di vertici e archi (Punto 1.c)

            self._view._txt_result.controls.append(
                ft.Text(f"Grafo creato con successo!\nNumero vertici: {n_nodes}\nNumero archi: {n_edges}",
                        color="green"))
            # RIEMPIO IL DROPDOWN DEI FILM DEL GRAFO
            self.fillDDNodoStart(categoria)
            self.fillDDNodoEnd(categoria)

        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore durante la creazione del grafo: {ex}", color="red"))
            # return
        self._view.update_page()

    def handleBestProdotti(self, e):
        self._view._txt_result.controls.clear()

        # C) 5 ARCHI CON PESO MAGGIORE
        top5 = self._model.get5ProdottiPiuVenduti()
        # self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f" 5 PRODOTTI PIù VENDUTI ", color="orange"))

        # self._view._txt_result.controls.append(ft.Text(f"{arco[0]}-->{arco[1]} (peso: {arco[2]["weight"]})"))
        for prodotto, valore in top5:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{prodotto.product_name} - "
                    f"{prodotto.model_year} with score {valore}"
                )
            )
        self._view.update_page()

    def handleCercaCammino(self, e):
        self._view._txt_result.controls.clear()

        if self._model.get_num_nodes() == 0 or self._model.get_num_edges() is None:
            self._view.create_alert("Creare prima il grafo!", color="red")
            return

        start = self._model.getProdottoById(self._view._ddProdStart.value)
        end= self._model.getProdottoById(self._view._ddProdEnd.value)
        # qui dovremmo fare i solti controlli sulla validità

        if start is None or end is None:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire i nodi iniziali e finali  per procedere!", color="red")
            )
            self._view.update_page()
            return
        k = self._view._txtInLun.value
        # qui dovremmo fare i solti controlli sulla validità

        try:
            kInt = int(k)
        except Exception as ex:
            self._view._txt_result.controls.append(
                ft.Text(f"Errore ! devi inserire un intero per procedere: {ex}", color="red")
            )
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.create_alert(
                "N deve essere un intero positivo.", color="red")
            return

        gruppo, punteggio = self._model.getGruppoProdotti(kInt,start,end)
        print("Prodotto iniziale:", start)
        print("Prodotto finale:", end)
        print("Lunghezza richiesta:", kInt)
        print("Percorso trovato:", gruppo)
        print("Punteggio:", punteggio)

        if len(gruppo) < kInt:
            self._view._txt_result.controls.append(
                ft.Text("Non esiste una selezione valida di K prodotti."))

        for prodotto in gruppo:
            self._view._txt_result.controls.append(
                ft.Text(
                    f"{prodotto.product_name} - "
                    f" {prodotto. model_year}")
            )

        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
