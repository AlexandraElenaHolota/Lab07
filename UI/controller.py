import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        situazioni = self._model.get_situazioni(self._mese)
        dizionario = {}
        dizionarioLocalita = self.ricerca_ricorsiva(situazioni, 0, dizionario)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(F"L'umidità media nel mese selezionato è: "))
        for key in dizionarioLocalita.keys():
            umidita = round(sum(dizionarioLocalita[key])/len(dizionarioLocalita[key]), 4)
            self._view.lst_result.controls.append(ft.Text(F"{key}: {umidita}"))
        self._view.update_page()

    def calcola_media(self, situazioni):
        somma = 0
        for s in situazioni:
            somma += s.umidita
        return somma/len(situazioni)

    def ricerca_ricorsiva(self, situazioni, i, dizionario):
        if i == len(situazioni):
            return dizionario
        else:
            if situazioni[i].localita not in dizionario:
                dizionario[situazioni[i].localita] = [situazioni[i].umidita]
                return self.ricerca_ricorsiva(situazioni, i+1, dizionario)
            else:
                dizionario[situazioni[i].localita].append(situazioni[i].umidita)
                return self.ricerca_ricorsiva(situazioni, i+1, dizionario)



    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza_ottima, costo = self._model.get_soluzione_migliore( self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {costo} ed è:"))
        for stop in sequenza_ottima:
            self._view.lst_result.controls.append(ft.Text(stop))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

