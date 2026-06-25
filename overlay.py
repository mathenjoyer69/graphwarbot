import tkinter as tk

class ScreenOverlay:
    def __init__(self, radius=15):
        self.root = None
        self.canvas = None
        self.coords: list[tuple[tuple[float, float], str]] = []

        self.radius = radius
        self.type1 = "double_abs"
        self.current_type = "double_abs"

    def start(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'black')

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.root.bind('<Escape>', lambda e: self.close())
        self.root.mainloop()

    def draw_circle(self, x, y, type2):
        if self.canvas and self.root:
            self.coords.append(((x, y), type2))
            self.redraw()

    def remove_last_circle(self):
        if self.coords and self.canvas:
            self.coords.pop()
            self.redraw()

    def set_current_type(self, new_type):
        self.current_type = new_type
        if self.canvas:
            self.redraw()

    def sort_coords(self):
        if self.coords:
            self.coords.sort(key=lambda point: point[0][0])

    def redraw(self):
        self.canvas.delete("all")
        self.sort_coords()

        self.canvas.create_text(
            30, 30,
            text=f"active type: {self.current_type}",
            fill='cyan',
            font=('Arial', 18, 'bold'),
            anchor='nw'
        )
        LNSI = 0 #LNSI = last_non_spike_index
        for i in range(1, len(self.coords)):
            prev_x, prev_y = self.coords[i - 1][0]
            curr_x, curr_y = self.coords[i][0]

            if self.coords[i-1][1] != "spike":
                LNSI = i-1

            match self.coords[i][1]:
                case "double_abs":
                    if self.coords[i-1][1] == "spike":
                        self.canvas.create_line(prev_x, self.coords[LNSI][0][1], curr_x, curr_y, fill='cyan', width=1)
                    else:
                        self.canvas.create_line(prev_x, prev_y, curr_x, curr_y, fill='cyan', width=1)

                case "step":
                    if self.coords[i-1][1] == "spike":
                        self.canvas.create_line(prev_x, self.coords[LNSI][0][1], curr_x, self.coords[LNSI][0][1], fill='cyan', width=1)
                        self.canvas.create_line(curr_x, self.coords[LNSI][0][1], curr_x, curr_y, fill='cyan', width=1)
                    else:
                        self.canvas.create_line(prev_x, prev_y, prev_x, curr_y, fill='cyan', width=1)
                        self.canvas.create_line(prev_x, curr_y, curr_x, curr_y, fill='cyan', width=1)

                case "spike":
                    if self.coords[i - 1][1] == "spike":
                        self.canvas.create_line(prev_x, self.coords[LNSI][0][1], curr_x, self.coords[LNSI][0][1], fill='cyan', width=1)
                        self.canvas.create_line(curr_x, self.coords[LNSI][0][1], curr_x, curr_y, fill='cyan', width=1)
                        self.canvas.create_line(curr_x, curr_y, curr_x, self.coords[LNSI][0][1], fill='cyan', width=1)
                    else:
                        self.canvas.create_line(prev_x, prev_y, curr_x, prev_y, fill='cyan', width=1)
                        self.canvas.create_line(curr_x, prev_y, curr_x, curr_y, fill='cyan', width=1)
                        self.canvas.create_line(curr_x, curr_y, curr_x, prev_y, fill='cyan', width=1)

        for t in self.coords:
            cx, cy = t[0]
            self.canvas.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, outline='cyan', width=2)

    def close(self):
        if self.root:
            self.root.quit()