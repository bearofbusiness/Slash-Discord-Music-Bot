import random
from asyncio import Event

from Song import Song


class Queue:
    """
    A class for containing and managing a list of Songs.

    ...

    Methods
    -------
    add(song: `Song`):
        Adds a Song to the end of the Queue.
    add(song: `Song`, index: `int`):
        Adds a Song to the Queue at the index.
    get(index: `int` | `None`):
        Retrieves Songs inside the Queue.
    shuffle():
        Shuffles the Queue.
    remove(index: `int`):
        Removes the Song at the index from the Queue and returns it.
    clear():
        Removes all Songs from the Queue.
    async wait_until_has_songs():
        Will wait asynchronously until the Queue has Songs inside it again.
    """
    def __init__(self) -> None:
        """
        Creates a Queue object.
        """
        self.queue = []
        self.has_songs = Event()

    def add(self, song: Song | list[Song]) -> None:
        """
        Adds a Song to the end of the Queue.
        
        Parameters
        ----------
        song : `Song` | `list[Song]`
            The Song or list of Songs to add to the Queue.
        """
        # If we were passed a Song or a list
        if isinstance(song, Song):
            self.queue.append(song)
            self.has_songs.set()
            return
        
        # Safety check for if we got an empty list
        if len(song) == 0:
            return
        self.queue.extend(song)
        self.has_songs.set()

    def add_at(self, song: Song, index: int) -> None:
        """
        Adds a Song to the Queue at the index.
        
        Parameters
        ----------
        song : `Song`
            The Song to add to the Queue.
        index : `int`
            The index to add the Song at.
        """
        self.queue.insert(index, song)
        self.has_songs.set()

    def get(self, index: int | None = None) -> Song | list[Song]:
        """
        Retrieves Songs inside the Queue.

        Parameters
        ----------
        index : `int` | `None`, optional
            The index of the Song to retrieve.

        Raises
        ------
        `IndexError`
            If the requested index is out of range.

        Returns
        -------
        `Song`:
            When provided with an integer, return the Song at that index.
        `list[Song]`:
            When provided with a NoneType, return all of the Songs in a list.

        """
        if index is None:
            return self.queue
        return self.queue[index]

    def shuffle(self) -> None:
        """
        Shuffles the Queue.

        This only changes the internal Song list of the Queue.
        """
        random.shuffle(self.queue)


    def remove(self, index: int) -> Song:
        """
        Removes the Song at the index from the Queue and returns it.
        
        Parameters
        ----------
        index : `int`
            The index to remove the Song from.

        Raises
        ------
        `IndexError`
            If the requested index is out of range.
        
        Returns
        -------
        `Song`:
            The removed Song.

        """
        song = self.queue.pop(index)
        # If this makes the queue empty
        if not self.queue:
            # Set the Event denoting the queue is empty
            self.has_songs.clear()
        return song

    def clear(self) -> None:
        """
        Removes all Songs from the Queue.
        """
        self.queue.clear()
        self.has_songs.clear()

    async def wait_until_has_songs(self) -> True:
        """
        Will wait asynchronously until the Queue has Songs inside it again.
        
        If the Queue has songs when this method is called, it will immediately return True.

        Returns
        -------
        `True`:
            Returns True once the wait is resolved.
        """
        return await self.has_songs.wait()
    
    def pop(self, index: int) -> Song:
        """
        Alias for remove(index).
        
        Parameters
        ----------
        index : `int`
            The index to remove the Song from.

        Raises
        ------
        `IndexError`
            If the requested index is out of range.
        
        Returns
        -------
        `Song`:
            The removed Song.

        """
        return self.remove(index)

    def __getitem__(self, index: int) -> Song:
        """
        Magic method for getting a Song or list of Songs from the Queue.
        
        Parameters
        ----------
        index: int
            The index of the Song to retrieve. also accepts int:int for slicing.

        Returns
        -------
            Song: 
                When provided with an integer, return the Song or list[Song] at that index.
        """
        return self.queue[index]
    
    def __setitem__(self, index: int, song: Song) -> None:
        """
        Magic method for setting a Song in the Queue.

        Parameters
        ----------
            index: int
                index of the Queue to set to.
            song: Song 
                Song to set at the index.
                
        """
        self.queue[index] = song

    def __delitem__(self, index: int) -> None:
        """
        Magic method for deleting a Song from the Queue.

        Parameters
        ----------
            index: int
                index of a Song in the Queue to delete.
        """
        del self.queue[index]

    def __contains__(self, song: Song) -> bool:
        """
        Magic method for checking if a Song is in the Queue.

        Parameters
        ----------
            song: Song
                Song to check for in the Queue.
        
        Returns
        -------
            bool:
                True if the Song is in the Queue, False otherwise.
        """
        return song in self.queue

    def __iter__(self) -> iter:
        """
        Magic method for iterating over the Queue.

        Returns
        -------
            iter:
                An iterator for the Queue.
        """
        return iter(self.queue)
    
    def __reversed__(self) -> iter:
        """
        Magic method for iterating over the Queue in reverse.

        Returns
        -------
            iter:
                An iterator for the Queue in reverse.
        """
        return reversed(self.queue)
    
    def __iadd__(self, song: Song | list[Song]) -> None:
        """
        Magic method for adding a Song to the Queue.

        Parameters
        ----------
            song: Song | list[Song]
                Song or list of Songs to add to the Queue.
        """
        self.add(song)

    def __len__(self) -> int:
        """
        Magic method for getting the length of the Queue.

        Returns
        -------
            int:
                The length of the Queue.
        """
        return len(self.queue)
    
    def __repr__(self) -> str:
        """
        Magic method for getting the representation of the Queue for debuging.

        Returns
        -------
            str:
                The representation of the Queue.
        """
        return str(self.queue)

    def __str__(self) -> str:
        """
        Magic method for getting the string representation of the Queue for users if needed.

        Returns
        -------
            str:
                The string representation of the Queue.
        """
        return str([str(song) for song in self.queue])