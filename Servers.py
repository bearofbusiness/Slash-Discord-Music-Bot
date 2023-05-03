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
        if isinstance(server, Player):
            for key, value in Servers.dict.items():
                if value == server:
                    del Servers.dict[key]
                    return
            print("Something went wrong, attempted to delete nonexistent Player.")
            return
        del Servers.dict[str(server)]
