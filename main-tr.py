import tkinter as tk
from tkinter import messagebox

from training import DigitTrainer, GRID_SIZE


CANVAS_SIZE = 280
CELL_SIZE = CANVAS_SIZE // GRID_SIZE
BRUSH_RADIUS = 1


class DigitGuesserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Digit Guesser")
        self.trainer = DigitTrainer()
        self.pixels = [0.0] * (GRID_SIZE * GRID_SIZE)
        self.last_cell = None

        self.canvas = tk.Canvas(
            root,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bg="white",
            cursor="pencil",
        )
        self.canvas.grid(row=0, column=0, columnspan=10, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.guess_text = tk.StringVar(value="Draw a digit, then click Guess.")
        tk.Label(root, textvariable=self.guess_text, font=("Arial", 14)).grid(
            row=1, column=0, columnspan=10, pady=(0, 8)
        )

        tk.Button(root, text="Guess", command=self.guess_digit).grid(
            row=2, column=0, columnspan=5, sticky="ew", padx=(10, 4), pady=4
        )
        tk.Button(root, text="Clear", command=self.clear_canvas).grid(
            row=2, column=5, columnspan=5, sticky="ew", padx=(4, 10), pady=4
        )

        tk.Label(root, text="Train as:").grid(row=3, column=0, columnspan=10, pady=(8, 2))
        for digit in range(10):
            tk.Button(
                root,
                text=str(digit),
                command=lambda value=digit: self.train_as(value),
                width=3,
            ).grid(row=4, column=digit, padx=2, pady=2)

        self.stats_text = tk.StringVar()
        tk.Label(root, textvariable=self.stats_text, justify="left").grid(
            row=5, column=0, columnspan=10, pady=10
        )
        self.update_stats()

    def start_draw(self, event):
        self.last_cell = None
        self.draw(event)

    def stop_draw(self, _event):
        self.last_cell = None

    def draw(self, event):
        x = max(0, min(GRID_SIZE - 1, event.x // CELL_SIZE))
        y = max(0, min(GRID_SIZE - 1, event.y // CELL_SIZE))
        current_cell = (x, y)

        if self.last_cell is None:
            cells = [current_cell]
        else:
            cells = self.cells_between(self.last_cell, current_cell)

        for cell_x, cell_y in cells:
            self.mark_cell(cell_x, cell_y)

        self.last_cell = current_cell

    def cells_between(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        steps = max(abs(end_x - start_x), abs(end_y - start_y), 1)
        cells = []

        for step in range(steps + 1):
            amount = step / steps
            x = round(start_x + (end_x - start_x) * amount)
            y = round(start_y + (end_y - start_y) * amount)
            cells.append((x, y))

        return cells

    def mark_cell(self, x, y):
        for dy in range(-BRUSH_RADIUS, BRUSH_RADIUS + 1):
            for dx in range(-BRUSH_RADIUS, BRUSH_RADIUS + 1):
                cell_x = x + dx
                cell_y = y + dy
                if 0 <= cell_x < GRID_SIZE and 0 <= cell_y < GRID_SIZE:
                    distance = abs(dx) + abs(dy)
                    value = 1.0 if distance == 0 else 0.55
                    index = cell_y * GRID_SIZE + cell_x
                    self.pixels[index] = max(self.pixels[index], value)
                    self.paint_cell(cell_x, cell_y, self.pixels[index])

    def paint_cell(self, x, y, value):
        shade = int(255 * (1 - value))
        color = f"#{shade:02x}{shade:02x}{shade:02x}"
        self.canvas.create_rectangle(
            x * CELL_SIZE,
            y * CELL_SIZE,
            (x + 1) * CELL_SIZE,
            (y + 1) * CELL_SIZE,
            fill=color,
            outline=color,
        )

    def guess_digit(self):
        if not any(self.pixels):
            self.guess_text.set("Draw something first.")
            return

        label, confidence = self.trainer.predict(self.pixels)
        if label is None:
            self.guess_text.set("No training data yet. Click the correct digit below.")
            return

        percent = round(confidence * 100)
        self.guess_text.set(f"My guess: {label} ({percent}% vote confidence)")

    def train_as(self, digit):
        if not any(self.pixels):
            messagebox.showinfo("Nothing to train", "Draw a digit first.")
            return

        self.trainer.add_sample(digit, self.pixels)
        self.guess_text.set(f"Saved this drawing as {digit}.")
        self.clear_canvas(keep_message=True)
        self.update_stats()

    def clear_canvas(self, keep_message=False):
        self.canvas.delete("all")
        self.pixels = [0.0] * (GRID_SIZE * GRID_SIZE)
        self.last_cell = None
        if not keep_message:
            self.guess_text.set("Draw a digit, then click Guess.")

    def update_stats(self):
        counts = self.trainer.label_counts()
        counts_text = "  ".join(f"{digit}:{counts[digit]}" for digit in range(10))
        self.stats_text.set(
            f"Training samples: {self.trainer.total_samples()}\n{counts_text}"
        )


def main():
    root = tk.Tk()
    DigitGuesserApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
