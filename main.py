import tkinter as tk
import random
import time
from threading import Thread

WIDTH, HEIGHT = 900, 550
BAR_AREA_H = 420
N_DEFAULT = 60
PADDING = 4

COLORS = {
    "bg":      "#0d0d0d",
    "bar":     "#00e5ff",
    "compare": "#ff4081",
    "swap":    "#ffeb3b",
    "sorted":  "#69ff47",
    "text":    "#ffffff",
    "accent":  "#00e5ff",
    "panel":   "#1a1a1a",
}

# ─── Algoritmos ───────────────────────────────────────────
def bubble_sort(arr, draw, delay):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            draw(arr, compare=[j, j+1])
            time.sleep(delay)
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                draw(arr, swap=[j, j+1])
                time.sleep(delay)
    draw(arr, done=True)

def selection_sort(arr, draw, delay):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            draw(arr, compare=[min_idx, j])
            time.sleep(delay)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw(arr, swap=[i, min_idx])
        time.sleep(delay)
    draw(arr, done=True)

def insertion_sort(arr, draw, delay):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            draw(arr, compare=[j, j+1])
            time.sleep(delay)
            arr[j+1] = arr[j]
            draw(arr, swap=[j, j+1])
            time.sleep(delay)
            j -= 1
        arr[j+1] = key
    draw(arr, done=True)

def merge_sort(arr, draw, delay, l=None, r=None):
    if l is None: l = 0
    if r is None: r = len(arr) - 1
    if l < r:
        m = (l + r) // 2
        merge_sort(arr, draw, delay, l, m)
        merge_sort(arr, draw, delay, m+1, r)
        _merge(arr, draw, delay, l, m, r)
    if l == 0 and r == len(arr) - 1:
        draw(arr, done=True)

def _merge(arr, draw, delay, l, m, r):
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    i = j = 0
    k = l
    while i < len(left) and j < len(right):
        draw(arr, compare=[l+i, m+1+j])
        time.sleep(delay)
        if left[i] <= right[j]:
            arr[k] = left[i]; i += 1
        else:
            arr[k] = right[j]; j += 1
        draw(arr, swap=[k])
        time.sleep(delay)
        k += 1
    while i < len(left):
        arr[k] = left[i]; i += 1; k += 1
        draw(arr, swap=[k-1]); time.sleep(delay)
    while j < len(right):
        arr[k] = right[j]; j += 1; k += 1
        draw(arr, swap=[k-1]); time.sleep(delay)

def quick_sort(arr, draw, delay, low=None, high=None, top=True):
    if low is None: low = 0
    if high is None: high = len(arr) - 1
    if low < high:
        pi = _partition(arr, draw, delay, low, high)
        quick_sort(arr, draw, delay, low, pi-1, False)
        quick_sort(arr, draw, delay, pi+1, high, False)
    if top:
        draw(arr, done=True)

def _partition(arr, draw, delay, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        draw(arr, compare=[j, high])
        time.sleep(delay)
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            draw(arr, swap=[i, j])
            time.sleep(delay)
    arr[i+1], arr[high] = arr[high], arr[i+1]
    draw(arr, swap=[i+1, high])
    time.sleep(delay)
    return i + 1

ALGORITHMS = {
    "Bubble Sort":    bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort":     merge_sort,
    "Quick Sort":     quick_sort,
}

# ─── App ──────────────────────────────────────────────────
class SortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer  //  by Mateus")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(False, False)

        self.arr = []
        self.running = False
        self.comparisons = 0
        self.swaps = 0
        self.start_time = None

        self._build_ui()
        self.generate_array()

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=BAR_AREA_H, bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack(padx=0, pady=(10, 0))

        stats_frame = tk.Frame(self.root, bg=COLORS["panel"], height=30)
        stats_frame.pack(fill="x")

        self.lbl_cmp = tk.Label(stats_frame, text="Comparações: 0", bg=COLORS["panel"], fg=COLORS["compare"], font=("Courier", 10, "bold"))
        self.lbl_cmp.pack(side="left", padx=20)

        self.lbl_swp = tk.Label(stats_frame, text="Trocas: 0", bg=COLORS["panel"], fg=COLORS["swap"], font=("Courier", 10, "bold"))
        self.lbl_swp.pack(side="left", padx=20)

        self.lbl_time = tk.Label(stats_frame, text="Tempo: 0.00s", bg=COLORS["panel"], fg=COLORS["sorted"], font=("Courier", 10, "bold"))
        self.lbl_time.pack(side="left", padx=20)

        self.lbl_status = tk.Label(stats_frame, text="● PRONTO", bg=COLORS["panel"], fg=COLORS["accent"], font=("Courier", 10, "bold"))
        self.lbl_status.pack(side="right", padx=20)

        ctrl = tk.Frame(self.root, bg=COLORS["bg"], pady=10)
        ctrl.pack(fill="x", padx=20)

        tk.Label(ctrl, text="ALGORITMO", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=0, sticky="w")
        self.algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = tk.OptionMenu(ctrl, self.algo_var, *ALGORITHMS.keys())
        algo_menu.config(bg=COLORS["panel"], fg=COLORS["accent"], font=("Courier", 11, "bold"), bd=0, activebackground=COLORS["bar"], highlightthickness=0, width=14)
        algo_menu["menu"].config(bg=COLORS["panel"], fg=COLORS["text"], font=("Courier", 10))
        algo_menu.grid(row=1, column=0, padx=(0, 30), sticky="w")

        tk.Label(ctrl, text="ELEMENTOS", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=1, sticky="w")
        self.n_var = tk.IntVar(value=N_DEFAULT)
        tk.Scale(ctrl, from_=10, to=150, orient="horizontal", variable=self.n_var, length=180, bg=COLORS["bg"], fg=COLORS["text"], troughcolor=COLORS["panel"],
                 highlightthickness=0, bd=0, font=("Courier", 9)).grid(row=1, column=1, padx=(0,30), sticky="w")

        tk.Label(ctrl, text="VELOCIDADE", bg=COLORS["bg"], fg=COLORS["text"], font=("Courier", 9)).grid(row=0, column=2, sticky="w")
        self.speed_var = tk.DoubleVar(value=50)
        tk.Scale(ctrl, from_=1, to=100, orient="horizontal", variable=self.speed_var, length=180, bg=COLORS["bg"], fg=COLORS["text"], troughcolor=COLORS["panel"],
                 highlightthickness=0, bd=0, font=("Courier", 9)).grid(row=1, column=2, padx=(0,30), sticky="w")

        btn_frame = tk.Frame(ctrl, bg=COLORS["bg"])
        btn_frame.grid(row=0, column=3, rowspan=2, sticky="e")

        self._btn(btn_frame, "GERAR", self.generate_array, COLORS["panel"], COLORS["accent"]).pack(side="left", padx=5)
        self.btn_sort = self._btn(btn_frame, "ORDENAR", self.start_sort, COLORS["accent"], COLORS["bg"])
        self.btn_sort.pack(side="left", padx=5)

        leg = tk.Frame(self.root, bg=COLORS["bg"])
        leg.pack(pady=(0, 8))
        for label, color in [("comparando", COLORS["compare"]), ("trocando",   COLORS["swap"]), ("ordenado",   COLORS["sorted"])]:
            tk.Label(leg, text="■ " + label, bg=COLORS["bg"], fg=color, font=("Courier", 9)).pack(side="left", padx=12)

    def _btn(self, parent, text, cmd, bg, fg):
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, font=("Courier", 11, "bold"), relief="flat", padx=14, pady=6, activebackground=COLORS["compare"],
                         activeforeground=COLORS["bg"], cursor="hand2")

    def generate_array(self):
        if self.running:
            return
        n = self.n_var.get()
        self.arr = list(range(1, n + 1))
        random.shuffle(self.arr)
        self.comparisons = 0
        self.swaps = 0
        self._update_stats()
        self.draw(self.arr)

    def draw(self, arr, compare=None, swap=None, done=False):
        self.canvas.delete("all")
        n = len(arr)
        if n == 0:
            return

        compare = set(compare or [])
        swap = set(swap or [])
        bar_w = WIDTH / n
        scale = (BAR_AREA_H - PADDING) / n

        for i, val in enumerate(arr):
            x0 = int(i * bar_w)
            x1 = int((i + 1) * bar_w) - 1
            bar_h = max(2, int(val * scale))
            y0 = BAR_AREA_H - bar_h
            y1 = BAR_AREA_H

            if done:
                color = COLORS["sorted"]
            elif i in swap:
                color = COLORS["swap"]
                self.swaps += 1
            elif i in compare:
                color = COLORS["compare"]
                self.comparisons += 1
            else:
                color = COLORS["bar"]

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self._update_stats()
        if done:
            self.lbl_status.config(text="✔ CONCLUÍDO", fg=COLORS["sorted"])
        self.canvas.update()

    def _update_stats(self):
        self.lbl_cmp.config(text=f"Comparações: {self.comparisons}")
        self.lbl_swp.config(text=f"Trocas: {self.swaps}")
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.lbl_time.config(text=f"Tempo: {elapsed:.2f}s")

    def start_sort(self):
        if self.running:
            return
        self.running = True
        self.comparisons = 0
        self.swaps = 0
        self.start_time = time.time()
        self.lbl_status.config(text="ORDENANDO...", fg=COLORS["swap"])
        self.btn_sort.config(state="disabled")

        algo = ALGORITHMS[self.algo_var.get()]
        delay = 0.001 + (1 - self.speed_var.get() / 100) * 0.15
        arr_copy = self.arr[:]

        def run():
            algo(arr_copy, self.draw, delay)
            self.arr = arr_copy
            self.running = False
            elapsed = time.time() - self.start_time
            self.lbl_time.config(text=f"Tempo: {elapsed:.2f}s")
            self.btn_sort.config(state="normal")

        Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SortVisualizer(root)
    root.mainloop()
