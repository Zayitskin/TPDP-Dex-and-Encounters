
import tkinter as tk

import json

from functools import partial
from collections import defaultdict as ddict

from ptypes import COLORS, generateMatchups

class Display(tk.Frame):

    def __init__(self, parent, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 1)
        self.grid_rowconfigure(4, weight = 1)
        self.grid_rowconfigure(5, weight = 1)
        self.grid_rowconfigure(6, weight = 1)
        self.grid_rowconfigure(7, weight = 1)
        self.grid_rowconfigure(8, weight = 1)
        self.grid_rowconfigure(9, weight = 1)
        self.grid_rowconfigure(10, weight = 1)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_columnconfigure(4, weight = 1)
        self.grid_columnconfigure(5, weight = 1)
        self.grid_columnconfigure(6, weight = 1)
        self.grid_columnconfigure(7, weight = 1)

        #Statics
        tk.Label(self, text = "Dex Number").grid(row = 0, column = 0, sticky = "ew")
        
        tk.Label(self, text = "HP").grid(row = 1, column = 0, sticky = "ew")
        tk.Label(self, text = "Focus Attack", fg = "#fb0127").grid(row = 1, column = 1, sticky = "ew")
        tk.Label(self, text = "Focus Defense").grid(row = 1, column = 2, sticky = "ew")
        tk.Label(self, text = "Spread Attack", fg = "#3c00da").grid(row = 1, column = 3, sticky = "ew")
        tk.Label(self, text = "Spread Defense").grid(row = 1, column = 4, sticky = "ew")
        tk.Label(self, text = "Speed", fg = "#008000").grid(row = 1, column = 5, sticky = "ew")
        tk.Label(self, text = "Base Stat Total").grid(row = 1, column = 6, sticky = "ew")
        tk.Label(self, text = "Cost").grid(row = 1, column = 7, sticky = "ew")

        #Dynamics
        self.id: tk.Label = tk.Label(self)
        self.id.grid(row = 0, column = 1, sticky = "ew")

        self.name: tk.Label = tk.Label(self)
        self.name.grid(row = 0, column = 2, columnspan = 4, sticky = "ew")

        self.type1: tk.Label = tk.Label(self)
        self.type1.grid(row = 0, column = 6, sticky = "ew")

        self.type2: tk.Label = tk.Label(self)
        self.type2.grid(row = 0, column = 7, sticky = "ew")

        self.hp: tk.Label = tk.Label(self)
        self.hp.grid(row = 2, column = 0, sticky = "ew")

        self.foatk: tk.Label = tk.Label(self, fg = "#fb0127")
        self.foatk.grid(row = 2, column = 1, sticky = "ew")

        self.spatk: tk.Label = tk.Label(self, fg = "#3c00da")
        self.spatk.grid(row = 2, column = 3, sticky = "ew")

        self.fodef: tk.Label = tk.Label(self)
        self.fodef.grid(row = 2, column = 2, sticky = "ew")

        self.spdef: tk.Label = tk.Label(self)
        self.spdef.grid(row = 2, column = 4, sticky = "ew")

        self.spd: tk.Label = tk.Label(self, fg = "#008000")
        self.spd.grid(row = 2, column = 5, sticky = "ew")

        self.bst: tk.Label = tk.Label(self)
        self.bst.grid(row = 2, column = 6, sticky = "ew")

        self.cost: tk.Label = tk.Label(self)
        self.cost.grid(row = 2, column = 7, sticky = "ew")

        self.abl1: tk.Label = tk.Label(self)
        self.abl1.grid(row = 3, column = 0, columnspan = 4, sticky = "ew")

        self.abl2: tk.Label = tk.Label(self)
        self.abl2.grid(row = 3, column = 4, columnspan = 4, sticky = "ew")

        self.quadW: tk.Frame = tk.Frame(self)
        self.quadW.grid(row = 4, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.quadW, text = "Quad weak to: ").grid(row = 0, column = 0)

        self.weak: tk.Frame = tk.Frame(self)
        self.weak.grid(row = 5, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.weak, text = "Weak to: ").grid(row = 0, column = 0)

        self.norm: tk.Frame = tk.Frame(self)
        self.norm.grid(row = 6, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.norm, text = "Normal damage from: ").grid(row = 0, column = 0)

        self.resist: tk.Frame = tk.Frame(self)
        self.resist.grid(row = 7, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.resist, text = "Resistant to: ").grid(row = 0, column = 0)

        self.quadR: tk.Frame = tk.Frame(self)
        self.quadR.grid(row = 8, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.quadR, text = "Quad resistant to: ").grid(row = 0, column = 0)

        self.immune: tk.Frame = tk.Frame(self)
        self.immune.grid(row = 9, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.immune, text = "Immune to: ").grid(row = 0, column = 0)

        self.encs: tk.Label = tk.Label(self)
        self.encs.grid(row = 10, column = 0, columnspan = 8, sticky = "ew")


    def loadMon(self, mon: dict) -> None:

        self.id.config(text = mon["id"])
        self.name.config(text = mon["name"])
        t1bc, t1tc = COLORS[mon["type1"]]
        self.type1.config(text = mon["type1"], bg = t1bc, fg = t1tc)
        t2bc, t2tc = COLORS[mon["type2"]]
        self.type2.config(text = mon["type2"], bg = t2bc, fg = t2tc)
        self.hp.config(text = mon["hp"])
        self.foatk.config(text = mon["foatk"])
        self.fodef.config(text = mon["fodef"])
        self.spatk.config(text = mon["spatk"])
        self.spdef.config(text = mon["spdef"])
        self.spd.config(text = mon["spd"])
        self.bst.config(text = mon["bst"])
        self.cost.config(text = mon["cost"])
        self.abl1.config(text = mon["abl1"])
        self.abl2.config(text = mon["abl2"])

        self.calcWeak((mon["type1"], mon["type2"]))
        
        self.encs.config(text = str(mon["encs"]).replace("], [", "\n").replace("[", "").replace("]", ""))

    def calcWeak(self, types: tuple[str, str]) -> None:

        self.quadW: tk.Frame = tk.Frame(self)
        self.quadW.grid(row = 4, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.quadW, text = "Quad weak to: ").grid(row = 0, column = 0)

        self.weak: tk.Frame = tk.Frame(self)
        self.weak.grid(row = 5, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.weak, text = "Weak to: ").grid(row = 0, column = 0)

        self.norm: tk.Frame = tk.Frame(self)
        self.norm.grid(row = 6, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.norm, text = "Normal damage from: ").grid(row = 0, column = 0)

        self.resist: tk.Frame = tk.Frame(self)
        self.resist.grid(row = 7, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.resist, text = "Resistant to: ").grid(row = 0, column = 0)

        self.quadR: tk.Frame = tk.Frame(self)
        self.quadR.grid(row = 8, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.quadR, text = "Quad resistant to: ").grid(row = 0, column = 0)

        self.immune: tk.Frame = tk.Frame(self)
        self.immune.grid(row = 9, column = 0, columnspan = 8, sticky = "ew")
        tk.Label(self.immune, text = "Immune to: ").grid(row = 0, column = 0)

        matchups: dict = generateMatchups(types)

        for i, t in enumerate(matchups["4x"]):
            tk.Label(self.quadW, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

        for i, t in enumerate(matchups["2x"]):
            tk.Label(self.weak, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

        for i, t in enumerate(matchups["1x"]):
            tk.Label(self.norm, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

        for i, t in enumerate(matchups["0.5x"]):
            tk.Label(self.resist, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

        for i, t in enumerate(matchups["0.25x"]):
            tk.Label(self.quadR, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

        for i, t in enumerate(matchups["0x"]):
            tk.Label(self.immune, text = t, bg = COLORS[t][0], fg = COLORS[t][1]).grid(row = 0, column = i + 1)

class Dex(tk.Frame):

    def __init__(self, parent, mons, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.mons = mons

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(2, weight = 10)

        self.puppetList: VerticalScrolledFrame = VerticalScrolledFrame(self)
        self.puppetList.grid(row = 1, column = 0, sticky = "news")

        self.display: Display = Display(self)
        self.display.grid(row = 0, column = 2, rowspan = 2, sticky = "new")

        self.searchVar: tk.StringVar = tk.StringVar(self)
        self.search: tk.Entry = tk.Entry(self, textvariable = self.searchVar)
        self.search.grid(row = 0, column = 0, sticky = "ew")

        self.buttons: list[tk.Button] = []
        self.buttonFrame: tk.Frame = tk.Frame(self.puppetList.interior)
        self.puppetList.interior.grid_columnconfigure(0, weight = 1)
        self.buttonFrame.grid_columnconfigure(0, weight = 1)
        for mon in self.mons:
            self.buttons.append(tk.Button(self.buttonFrame,
                                          text = mon["name"],
                                       ))
        for index, button in enumerate(self.buttons):
            button.grid(row = index, column = 0, sticky = "ew")
            button.properLocation = index
            button.config(command = partial(self.loadMon, button.properLocation))

        self.buttonFrame.grid(row = 0, column = 0, sticky = "ew")

        self.searchVar.trace_add("write", self.searchCallback)

    def searchCallback(self, var: str, index: str, mode: str) -> None:

        s: str = self.searchVar.get()
        if s == "":
            return
        for button in self.buttons:
            if s not in button.cget("text").lower():
                button.grid_forget()
            else:
                button.grid(row = button.properLocation, column = 0, sticky = "ew")

    def loadMon(self, monid: int) -> None:

        self.display.loadMon(self.mons[monid])

class ChecklistByIndex(tk.Frame):

    def __init__(self, parent, cl, mons, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 0)

        self.puppetList: tk.Canvas = tk.Canvas(self)
        self.puppetList.grid(row = 0, column = 0, sticky = "news")

        self.plsb: tk.Scrollbar = tk.Scrollbar(self)
        self.plsb.grid(row = 0, column = 1, sticky = "ns")

class ChecklistByArea(tk.Frame):

    def __init__(self, parent, cl, mons, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

        self.cl: dict = cl
        self.areas: ddict = ddict(list)
        for mon in mons:
            if "Normal" in mon["name"]:
                for area in mon["encs"]:
                    self.areas[area[0]].append((mon["name"], area[1]))

        self.searchVar: tk.StringVar = tk.StringVar(self)
        self.search: tk.Entry = tk.Entry(self, textvariable = self.searchVar)
        self.search.grid(row = 0, column = 0, sticky = "ew")

        self.vsf: VerticalScrolledFrame = VerticalScrolledFrame(self)
        self.vsf.grid(row = 1, column = 0, sticky = "news")

        self.display: AreaDisplay = AreaDisplay(self, self.cl)
        self.display.grid(row = 1, column = 1, sticky = "news")

        self.buttons: list[tk.Button] = []
        self.buttonFrame: tk.Frame = tk.Frame(self.vsf.interior)
        self.vsf.interior.grid_columnconfigure(0, weight = 1)
        self.vsf.grid_columnconfigure(0, weight = 1)        

        for area in self.areas:
            self.buttons.append(tk.Button(self.buttonFrame,
                                          text = area,
                                       ))
        for index, button in enumerate(self.buttons):
            button.grid(row = index, column = 0, sticky = "ew")
            button.properLocation = index
            button.config(command = partial(self.loadArea, button.properLocation))

        self.buttonFrame.grid(row = 0, column = 0, sticky = "ew")

        self.save: tk.Button = tk.Button(self, text = "Save", command = self.saveCL)
        self.save.grid(row = 0, column = 1, sticky = "ew")
        

        self.searchVar.trace_add("write", self.searchCallback)

    def searchCallback(self, var: str, index: str, mode: str) -> None:

        s: str = self.searchVar.get()
        if s == "":
            return
        for button in self.buttons:
            if s not in button.cget("text").lower():
                button.grid_forget()
            else:
                button.grid(row = button.properLocation, column = 0, sticky = "ew")

    def loadArea(self, areaid: int) -> None:

        self.display.clear()
        for enc in self.areas[self.buttons[areaid].cget("text")]:
            self.display.add(enc)

    def saveCL(self):
        with open("checklist.json", "w") as fc:
            json.dump(self.cl, fc)

class AreaDisplay(tk.Frame):

    def __init__(self, parent, cl, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.encs: list[Encounter] = []
        self.cl: dict = cl

    def clear(self) -> None:

        for enc in self.encs:
            enc.grid_forget()
        self.encs = []

    def add(self, enc: tuple[str, str]) -> None:

        self.encs.append(Encounter(self, enc[0], enc[1], self.cl))
        self.encs[-1].grid(row = len(self.encs) - 1, column = 0, sticky = "ew")

class Encounter(tk.Frame):

    def __init__(self, parent, name, rate, cl, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.cl = cl

        self.checkvalue: tk.BooleanVar = tk.BooleanVar(self)
        self.checkbutton = tk.Checkbutton(self, offvalue = False, onvalue = True, variable = self.checkvalue)
        if cl[name]:
            self.checkbutton.select()
        else:
            self.checkbutton.deselect()
        self.checkbutton.grid(row = 0, column = 0)

        self.checkvalue.trace_add("write", self.updateCL)
        
        self.name: tk.Label = tk.Label(self, text = name)
        self.name.grid(row = 0, column = 1)
        self.rate: tk.Label = tk.Label(self, text = rate)
        self.rate.grid(row = 0, column = 2)

    def updateCL(self, var: str, index: str, mode: str) -> None:

        self.cl[self.name.cget("text")] = self.checkvalue.get()

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    https://stackoverflow.com/questions/31762698/dynamic-button-with-scrollbar-in-tkinter-python
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
