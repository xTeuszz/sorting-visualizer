from config import COLORS, BAR_AREA_H, WIDTH, PADDING


class Visualizer:
    def __init__(self, canvas, lbl_cmp, lbl_swp, lbl_time, lbl_status):
        self.canvas     = canvas
        self.lbl_cmp    = lbl_cmp
        self.lbl_swp    = lbl_swp
        self.lbl_time   = lbl_time
        self.lbl_status = lbl_status

        self.comparisons = 0
        self.swaps       = 0
        self.start_time  = None

    def reset_stats(self):
        self.comparisons = 0
        self.swaps       = 0
        self.start_time  = None
        self._update_labels()

    def draw(self, arr, compare=None, swap=None, done=False):
        self.canvas.delete("all")
        n = len(arr)
        if n == 0:
            return

        compare = set(compare or [])
        swap    = set(swap    or [])
        bar_w   = WIDTH / n
        scale   = (BAR_AREA_H - PADDING) / n

        for i, val in enumerate(arr):
            x0    = int(i * bar_w)
            x1    = int((i + 1) * bar_w) - 1
            bar_h = max(2, int(val * scale))
            y0    = BAR_AREA_H - bar_h
            y1    = BAR_AREA_H

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

        self._update_labels()

        if done:
            self.lbl_status.config(text="✔ CONCLUÍDO", fg=COLORS["sorted"])

        self.canvas.update()

    def _update_labels(self):
        import time as _time
        self.lbl_cmp.config(text=f"Comparações: {self.comparisons}")
        self.lbl_swp.config(text=f"Trocas: {self.swaps}")
        if self.start_time:
            elapsed = _time.time() - self.start_time
            self.lbl_time.config(text=f"Tempo: {elapsed:.2f}s")
