import json
import math
import os
from collections import Counter


GRID_SIZE = 28
PIXEL_COUNT = GRID_SIZE * GRID_SIZE
MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "digit_data.json")


class DigitTrainer:
    def __init__(self, model_path=MODEL_FILE, k=3):
        self.model_path = model_path
        self.k = k
        self.samples = []
        self.load()

    def load(self):
        if not os.path.exists(self.model_path):
            self.samples = []
            return

        with open(self.model_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.samples = data.get("samples", [])

    def save(self):
        data = {"samples": self.samples}
        with open(self.model_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def add_sample(self, label, pixels):
        label = int(label)
        if label < 0 or label > 9:
            raise ValueError("Label must be a digit from 0 to 9.")

        clean_pixels = self.normalize_pixels(pixels)
        self.samples.append({"label": label, "pixels": clean_pixels})
        self.save()

    def predict(self, pixels):
        if not self.samples:
            return None, 0.0

        clean_pixels = self.normalize_pixels(pixels)
        distances = []

        for sample in self.samples:
            distance = self._distance(clean_pixels, sample["pixels"])
            distances.append((distance, sample["label"]))

        nearest = sorted(distances, key=lambda item: item[0])[: self.k]
        votes = Counter(label for _, label in nearest)
        best_label, vote_count = votes.most_common(1)[0]
        confidence = vote_count / len(nearest)
        return best_label, confidence

    def label_counts(self):
        counts = Counter(sample["label"] for sample in self.samples)
        return {digit: counts.get(digit, 0) for digit in range(10)}

    def total_samples(self):
        return len(self.samples)

    def normalize_pixels(self, pixels):
        pixels = [float(value) for value in pixels]
        if len(pixels) != PIXEL_COUNT:
            raise ValueError(f"Expected {PIXEL_COUNT} pixels.")

        biggest = max(pixels) if pixels else 0
        if biggest <= 0:
            return [0.0] * PIXEL_COUNT

        pixels = [value / biggest for value in pixels]
        return self._center_image(pixels)

    def _center_image(self, pixels):
        used = [
            (index % GRID_SIZE, index // GRID_SIZE, value)
            for index, value in enumerate(pixels)
            if value > 0.05
        ]
        if not used:
            return pixels

        min_x = min(x for x, _, _ in used)
        max_x = max(x for x, _, _ in used)
        min_y = min(y for _, y, _ in used)
        max_y = max(y for _, y, _ in used)

        width = max_x - min_x + 1
        height = max_y - min_y + 1
        offset_x = (GRID_SIZE - width) // 2 - min_x
        offset_y = (GRID_SIZE - height) // 2 - min_y

        centered = [0.0] * PIXEL_COUNT
        for x, y, value in used:
            new_x = x + offset_x
            new_y = y + offset_y
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                centered[new_y * GRID_SIZE + new_x] = max(
                    centered[new_y * GRID_SIZE + new_x], value
                )

        return centered

    def _distance(self, a, b):
        return math.sqrt(sum((left - right) ** 2 for left, right in zip(a, b)))
