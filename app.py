import tkinter as tk
import random
import time
from threading import Thread

from config     import COLORS, WIDTH, BAR_AREA_H, N_DEFAULT
from algorithms import ALGORITHMS
from visualizer import Visualizer


class SortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer  //  by Mateus")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)

        self.arr     = []
        self.running = False

        self._build_ui()
        self.generate_array()

    # ── UI ────────────────────────────────────────────────

    def _build_ui(self):
        canvas = tk.Canvas(
            self.root, width=WIDTH, height=BAR_AREA_H,
            bg=COLORS["bg"], highlightthickness=0,
        )
        canvas.pack(padx=0, pady=(10, 0))

        # Stats bar
        stats = tk.Frame(self.root, bg=COLORS["panel"], height=30)
        stats.pack(fill="x")

        lbl_cmp    = tk.Label(stats, text="Comparações: 0", bg=COLORS["panel"], fg=COLORS["compare"], font=("Courier", 10, "bold"))
        lbl_swp    = tk.Label(stats, text="Trocas: 0",      bg=COLORS["panel"], fg=COLORS["swap"],    font=("Courier", 10, "bold"))
        lbl_time   = tk.Label(stats, text="Tempo: 0.00s",   bg=COLORS["panel"], fg=COLORS["sorted"],  font=("Courier", 10, "bold"))
        lbl_status = tk.Label(stats, text="● PRONTO",       bg=COLORS["panel"], fg=COLORS["accent"],  font=("Courier", 10, "bold"))

        lbl_cmp.pack(side="left",  padx=20)
        lbl_swp.pack(side="left",  padx=20)
        lbl_time.pack(side="left", padx=20)
        lbl_status.pack(side="right", padx=20)

        self.lbl_status = lbl_status
        self.lbl_time   = lbl_time

        self.viz = Visualizer(canvas, lbl_cmp, lbl_swp, lbl_time, lbl_status)

        # Controls
        ctrl = tk.Frame(self.root, bg=COLORS["bg"], pady=10)
        ctrl.pack(fill="x", padx=20)

        tk.Label(ctrl, text="ALGORITMO", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=0, sticky="w")
        self.algo_var = tk.StringVar(value="Bubble Sort")
        menu = tk.OptionMenu(ctrl, self.algo_var, *ALGORITHMS.keys())
        menu.config(bg=COLORS["panel"], fg=COLORS["accent"], font=("Courier", 11, "bold"),
                    bd=0, activebackground=COLORS["bar"], highlightthickness=0, width=14)
        menu["menu"].config(bg=COLORS["panel"], fg=COLORS["text"], font=("Courier", 10))
        menu.grid(row=1, column=0, padx=(0, 30), sticky="w")

        tk.Label(ctrl, text="ELEMENTOS", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=1, sticky="w")
        self.n_var = tk.IntVar(value=N_DEFAULT)
        tk.Scale(ctrl, from_=10, to=150, orient="horizontal", variable=self.n_var, length=180,
                 bg=COLORS["bg"], fg=COLORS["text"], troughcolor=COLORS["panel"],
                 highlightthickness=0, bd=0, font=("Courier", 9)).grid(row=1, column=1, padx=(0, 30), sticky="w")

        tk.Label(ctrl, text="VELOCIDADE", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=2, sticky="w")
        self.speed_var = tk.DoubleVar(value=50)
        tk.Scale(ctrl, from_=1, to=100, orient="horizontal", variable=self.speed_var, length=180,
                 bg=COLORS["bg"], fg=COLORS["text"], troughcolor=COLORS["panel"],
                 highlightthickness=0, bd=0, font=("Courier", 9)).grid(row=1, column=2, padx=(0, 30), sticky="w")

        btn_frame = tk.Frame(ctrl, bg=COLORS["bg"])
        btn_frame.grid(row=0, column=3, rowspan=2, sticky="e")
        self._btn(btn_frame, "GERAR",    self.generate_array, COLORS["panel"],  COLORS["accent"]).pack(side="left", padx=5)
        self.btn_sort = self._btn(btn_frame, "ORDENAR", self.start_sort,  COLORS["accent"], COLORS["bg"])
        self.btn_sort.pack(side="left", padx=5)

        # Legend
        leg = tk.Frame(self.root, bg=COLORS["bg"])
        leg.pack(pady=(0, 8))
        for label, color in [("comparando", COLORS["compare"]), ("trocando", COLORS["swap"]), ("ordenado", COLORS["sorted"])]:
            tk.Label(leg, text="■ " + label, bg=COLORS["bg"], fg=color, font=("Courier", 9)).pack(side="left", padx=12)

    def _btn(self, parent, text, cmd, bg, fg):
        return tk.Button(
            parent, text=text, command=cmd,
            bg=bg, fg=fg, font=("Courier", 11, "bold"),
            relief="flat", padx=14, pady=6,
            activebackground=COLORS["compare"],
            activeforeground=COLORS["bg"],
            cursor="hand2",
        )

    # ── Actions ───────────────────────────────────────────

    def generate_array(self):
        if self.running:
            return
        n = self.n_var.get()
        self.arr = list(range(1, n + 1))
        random.shuffle(self.arr)
        self.viz.reset_stats()
        self.viz.draw(self.arr)

    def start_sort(self):
        if self.running:
            return
        self.running = True
        self.viz.reset_stats()
        self.viz.start_time = time.time()
        self.lbl_status.config(text="ORDENANDO...", fg=COLORS["swap"])
        self.btn_sort.config(state="disabled")

        algo      = ALGORITHMS[self.algo_var.get()]
        delay     = 0.001 + (1 - self.speed_var.get() / 100) * 0.15
        arr_copy  = self.arr[:]

        def run():
            algo(arr_copy, self.viz.draw, delay)
            self.arr     = arr_copy
            self.running = False
            elapsed = time.time() - self.viz.start_time
            self.lbl_time.config(text=f"Tempo: {elapsed:.2f}s")
            self.btn_sort.config(state="normal")

        Thread(target=run, daemon=True).start()
