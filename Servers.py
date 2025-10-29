from __future__ import annotations
# Use annotations here to keep the type suggestions without causing a circular import

import Player

class Servers():
    """
    Static class that contains a dict of all Players and what guilds they are associated with.

    Because this class is static it is accessible without any variables yet still persists data.

    ...

    Methods
    -------
    add(server: `int`, player: `Player`):
        Registers a Player to the provided guild id.
    get_player(server: `int`):
        Get the Player associated with the provided guild id, if any.
    set_player(server: `int`, player: `Player`):
        Replaces/registers a Player to the provided guild id.
    remove(server: `int` | `Player`):
        Unregisters a Player by guild id or Object.
    """
    dict = {}

    @staticmethod
    def add(server: int, player: Player.Player) -> None:
        """
        Registers a Player to the provided guild id.
        
        Parameters
        ----------
        server : `int`
            The guild ID to associate the Player with.
        player : `Player`
            The player to be associated with the guild ID.
        """
        Servers.dict[server] = player

    @staticmethod
    def get_player(server: int) -> Player.Player:
        """
        Get the Player associated with the provided guild id, if any.

        Parameters
        ----------
        server: `int`
            The guild id to search for a Player under.

        Returns
        -------
        player : Player or None
            The Player associated with the guild or None if there is no Player associated with the guild id.
        """
        return Servers.dict.get(server)

    @staticmethod
    def set_player(server: int, player: Player.Player) -> None:
        """
        Replaces/registers a Player to the provided guild id.        

        Parameters
        ----------
        server : `int`
            The guild ID to associate the Player with.
        player : `Player`
            The player to be associated with the guild ID.
        """
        Servers.dict.update({server : player})

    @staticmethod
    def remove(server: Player.Player | int) -> None:
        """
        Unregisters a Player by guild id or Object.

        Parameters
        ----------
        server : `int` | `Player`
            The id of the guild associated with the Player or the Player itself.

        Raises
        ------
        `IndexError`
            If the id or Player were not found within the dict.

        """
        #TODO find a faster method than this for removing by Player
        #O(n) in the worst case. (I think?)
        if isinstance(server, Player.Player):
            for key, value in Servers.dict.items():
                if value == server:
                    del Servers.dict[key]
                    return
            raise IndexError("Something went wrong, attempted to delete nonexistent Player.")
        del Servers.dict[str(server)]
