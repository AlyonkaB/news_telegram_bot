import json
import os


class NewsManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.seen_titles = set()
        self.load_titles()

    def load_titles(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.seen_titles = set(json.load(file)["data"])

    def save_title(self, title):
        self.seen_titles.add(title)
        with open(self.file_path, "w") as file:
            data = {"data": list(self.seen_titles)}
            json.dump(data, file, indent=4)

    def is_new_title(self, title):
        if title not in self.seen_titles:
            return True
        return False
