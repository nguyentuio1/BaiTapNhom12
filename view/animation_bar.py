import tkinter as tk


class AnimationBar(tk.Frame):
    def __init__(self, master, on_frame_change=None):
        super().__init__(master)
        self.on_frame_change = on_frame_change
        self.frames = []
        self.index = 0
        self._playing = False
        self._after_id = None

        self.btn_first = tk.Button(self, text="⏮", command=self.first, width=3)
        self.btn_prev = tk.Button(self, text="◀", command=self.prev, width=3)
        self.btn_play = tk.Button(self, text="▶", command=self.toggle_play, width=3)
        self.btn_next = tk.Button(self, text="▶|", command=self.next, width=3)
        self.btn_last = tk.Button(self, text="⏭", command=self.last, width=3)
        for b in (self.btn_first, self.btn_prev, self.btn_play, self.btn_next, self.btn_last):
            b.pack(side=tk.LEFT, padx=2, pady=2)

        tk.Label(self, text="  Tốc độ:").pack(side=tk.LEFT)
        self.speed = tk.Scale(self, from_=100, to=2000, orient=tk.HORIZONTAL, length=200,
                              showvalue=False)
        self.speed.set(800)
        self.speed.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Bước 0/0", width=15)
        self.label.pack(side=tk.LEFT, padx=10)

    def load(self, frames):
        self.stop()
        self.frames = frames
        self.index = 0
        self._update()
        self._emit()

    def _emit(self):
        if 0 <= self.index < len(self.frames) and self.on_frame_change:
            self.on_frame_change(self.frames[self.index], self.index, len(self.frames))

    def _update(self):
        cur = self.index + 1 if self.frames else 0
        self.label.config(text=f"Bước {cur}/{len(self.frames)}")

    def first(self):
        self.index = 0
        self._update(); self._emit()

    def last(self):
        self.index = max(0, len(self.frames) - 1)
        self._update(); self._emit()

    def prev(self):
        if self.index > 0:
            self.index -= 1
            self._update(); self._emit()

    def next(self):
        if self.index < len(self.frames) - 1:
            self.index += 1
            self._update(); self._emit()

    def toggle_play(self):
        if self._playing:
            self.stop()
        else:
            self.play()

    def play(self):
        if not self.frames:
            return
        self._playing = True
        self.btn_play.config(text="⏸")
        self._tick()

    def stop(self):
        self._playing = False
        self.btn_play.config(text="▶")
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _tick(self):
        if not self._playing:
            return
        if self.index >= len(self.frames) - 1:
            self.stop()
            return
        self.index += 1
        self._update(); self._emit()
        self._after_id = self.after(self.speed.get(), self._tick)
