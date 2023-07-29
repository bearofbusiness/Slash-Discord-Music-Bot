# imports for classes from other files
from Player import Player

class Servers():
    """
    Static class that contains a dict of all Players and what guilds they are associated with.

    Because this class is static it is accessible without any variables yet still persists data.

    ...

    Methods
    -------
    add(server: int, player: Player):
        Registers a Player to the provided guild id.
    get_player(server: int):
        Get the Player associated with the provided guild id, if any.
    set_player(server: int, player: Player):
        Replaces/registers a Player to the provided guild id.
    remove(server: id | Player):
        Unregisters a Player by guild id or Object.
    """
    dict = {}

    @staticmethod
    def add(server: int, player: Player) -> None:
        """
        Registers a Player to the provided guild id.
        
        Parameters
        ----------
        server : int
            The guild ID to associate the Player with.
        player : Player
            The player to be associated with the guild ID.
        """
        Servers.dict[server] = player

    @staticmethod
    def get_player(server: int) -> Player | None:
        """
        Get the Player associated with the provided guild id, if any.

        Parameters
        ----------
        server: int
            The guild id to search for a Player under.

        Return
        ------
        Player:
            The Player associated with the guild.
        None:
            Returned if there is no Player associated with the guild id.
        """
        return Servers.dict.get(server)

    @staticmethod
    def set_player(server: int, player: Player):
        """
        Replaces/registers a Player to the provided guild id.        

        Parameters
        ----------
        server : int
            The guild ID to associate the Player with.
        player : Player
            The player to be associated with the guild ID.
        """
        Servers.dict.update({server : player})

    @staticmethod
    def remove(server: int | Player) -> None:
        """
        Unregisters a Player by guild id or Object.

        Parameters
        ----------
        server : int | Player
            The id of the guild associated with the Player or the Player itself.

        Raises
        ------
        IndexError
            If the id or Player were not found within the dict.

        """
        #TODO find a faster method than this for removing by Player
        #O(n) in the worst case. (I think?)
        if isinstance(server, Player):
            for key, value in Servers.dict.items():
                if value == server:
                    del Servers.dict[key]
                    return
            print("Something went wrong, attempted to delete nonexistent Player.")
            raise IndexError
        del Servers.dict[str(server)]
