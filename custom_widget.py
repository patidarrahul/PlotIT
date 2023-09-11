import tkinter as tk
from tkinter import ttk

class CustomButton(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        button = tk.Button(self,relief ='solid', bg = 'white',*args, **kwargs)
        button.pack(fill="both", expand=2, padx=0.5, pady=0.5)
        self.configure(background = 'lightblue')


class CustomEntry(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        entry = tk.Entry(self,relief ='sunken',*args, **kwargs)
        entry.pack(fill="both", expand=2, padx=1, pady=1)
        self.configure(background = '#28486B')


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg = 'white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.bind_mousewheel(self.canvas)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def bind_mousewheel(self, widget):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        widget.bind("<MouseWheel>", _on_mousewheel)


