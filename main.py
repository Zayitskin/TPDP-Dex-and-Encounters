

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as Tkfont

from widgets import Dex, ChecklistByIndex, ChecklistByArea

import os.path
import json

class App(tk.Tk):

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        if not os.path.exists("mons.json"):
            print("Puppet database does not exist, creating now.")
            from scraper import scrapeSoD
            scrapeSoD()

        if not os.path.exists("checklist.json"):
            print("No default checklist found, creating one.")
            from checklists import createEmptyChecklist
            createEmptyChecklist()

        with open("mons.json") as fm:
            self.mons: list = json.load(fm)
            
        with open("checklist.json") as fc:
            self.cl: dict = json.load(fc)

        default_font = Tkfont.nametofont("TkDefaultFont")
        default_font.configure(size = 12)
        
        self.notebook: ttk.Notebook = ttk.Notebook(self)
        self.notebook.pack(fill = "both", expand = True)
        self.dex: Dex = Dex(self.notebook, self.mons)
        self.notebook.add(self.dex, text = "PuppetDex")
        #self.clbi: ChecklistByIndex = ChecklistByIndex(self.notebook, self.cl, self.mons)
        #self.notebook.add(self.clbi, text = "Checklist By Index")
        self.clba: ChecklistByArea = ChecklistByArea(self.notebook, self.cl, self.mons)
        self.notebook.add(self.clba, text = "Checklist By Area")


if __name__ == "__main__":

    app: App = App()
    app.title("TPDP Companion App")
    app.geometry("1000x800")
    app.mainloop()
