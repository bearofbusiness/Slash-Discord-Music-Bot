import random
from asyncio import Event

from Song import Song


class Queue:
    """
    A class for containing and managing a list of Songs.

    ...

    Methods
    -------
    add(song: Song):
        Adds a Song to the end of the Queue.
    add(song: Song, index: int):
        Adds a Song to the Queue at the index.
    get(index: int | None):
        Retrieves Songs inside the Queue.
    shuffle():
        Shuffles the Queue.
    remove(index: int):
        Removes the Song at the index from the Queue and returns it.
    clear():
        Removes all Songs from the Queue.
    async wait_until_has_songs():
        Will wait asynchronously until the Queue has Songs inside it again.
    """
    def __init__(self) -> None:
        self.list = []
        self.has_songs = Event()

    def add(self, song: Song) -> None:
        """
        Adds a Song to the end of the Queue.
        
        Parameters
        ----------
        song : Song
            The Song to add to the Queue.
        """
        self.list.append(song)
        self.has_songs.set()

    def add_at(self, song: Song, index: int) -> None:
        """
        Adds a Song to the Queue at the index.
        
        Parameters
        ----------
        song : Song
            The Song to add to the Queue.
        index : int
            The index to add the Song at.
        """
        self.list.insert(index, song)
        self.has_songs.set()

    def get(self, index: int | None = None) -> Song | list[Song]:
        """
        Retrieves Songs inside the Queue.

        Parameters
        ----------
        index : int | None, optional
            The index of the Song to retrieve.

        Raises
        ------
        IndexError
            If the requested index is out of range.

        Returns
        -------
        Song:
            When provided with an integer, return the Song at that index.
        list[Song]:
            When provided with a NoneType, return all of the Songs in a list.

        """
        if index is None:
            return self.list
        return self.list[index]

    def shuffle(self) -> None:
        """
        Shuffles the Queue.

        This only changes the internal Song list of the Queue.
        """
        random.shuffle(self.list)


    def remove(self, index: int) -> Song:
        """
        Removes the Song at the index from the Queue and returns it.
        
        Parameters
        ----------
        index : int
            The index to remove the Song from.

        Raises
        ------
        IndexError
            If the requested index is out of range.
        
        Returns
        -------
        Song:
            The removed Song.

        """
        song = self.list.pop(index)
        # If this makes the list empty
        if not self.list:
            # Set the Event denoting the list is empty
            self.has_songs.clear()
        return song

    def clear(self) -> None:
        """
        Removes all Songs from the Queue.
        """
        self.list.clear()
        self.has_songs.clear()

    async def wait_until_has_songs(self) -> True:
        """
        Will wait asynchronously until the Queue has Songs inside it again.
        
        If the Queue has songs when this method is called, it will immediately return True.

        Returns
        -------
        True:
            Returns True once the wait is resolved.
        """
        return await self.has_songs.wait()

    def __len__(self) -> int:
        return len(self.list)

    def __str__(self) -> str:
        return str([str(song) for song in self.list])
