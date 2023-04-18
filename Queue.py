import random
from asyncio import Event

from Song import Song


class Queue:
    def __init__(self) -> None:
        self.list = []
        self.has_songs = Event()

    def add(self, song: Song) -> None:
        self.list.append(song)
        self.has_songs.set()

    def add_at(self, song: Song, index: int) -> None:
        self.list.insert(index, song)
        self.has_songs.set()

    def get(self, index: int | None = None) -> Song | list:
        if index is None:
            return self.list
        return self.list[index]

    def shuffle(self) -> None:
        temp_list = self.list.copy()
        temp_list.pop(0)
        random.shuffle(temp_list)
        self.list = [self.list[0]] + temp_list

    def remove(self, index: int) -> Song:
        song = self.list.pop(index)
        # If this makes the list empty
        if not self.list:
            # Set the Event denoting the list is empty
            self.has_songs.clear()
        return song

    def clear(self) -> None:
        self.list.clear()

    async def wait_until_has_songs(self) -> True:
        return await self.has_songs.wait()

    def __len__(self) -> int:
        return len(self.list)

    def __str__(self) -> str:
        return str([str(song) for song in self.list])
