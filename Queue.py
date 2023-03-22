import Song
import random


class Queue:
    def __init__(self):
        self.list = []

    def add(self, song: Song) -> None:
        self.list.append(song)

    def add_at(self, song: Song, index) -> None:
        self.list.insert(index, song)

    def get(self, index: int) -> Song:
        return self.list[index]
    
    def get(self) -> list:
        return self.list

    def shuffle(self) -> None:
        random.shuffle(self.list)

    def remove(self, index: int) -> Song:
        return self.list.pop(index)

    def __len__(self) -> int:
        return len(self.list)
