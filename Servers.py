# imports for classes from other files
from Player import Player

class Servers():
    dict = {}

    @staticmethod
    def add(server: int, player: Player) -> None:
        Servers.dict[server] = player

    @staticmethod
    def get_player(server: int) -> Player:
        return Servers.dict.get(server)

    @staticmethod
    def set_player(server: int, player: Player):
        Servers.dict.update({server : player})

    @staticmethod
    def remove(server: int | Player) -> None:
        if type(server) == "Player":
            # Use a dict comprehension to remove the Player from the dict
            Servers.dict.items = {key:val for key, val in Servers.dict.items() if val != server}
            return
        del Servers.dict[str(server)]
