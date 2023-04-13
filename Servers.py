# imports for classes from other files
from Player import Player

class Servers():
    dict = {}

    @staticmethod
    def add(server: str | int, player: Player) -> None:
        Servers.dict[str(server)] = player

    @staticmethod
    def get_player(server: str | int) -> Player:
        return Servers.dict.get(str(server))

    @staticmethod
    def set_player(server: str | int, player: Player):
        Servers.dict.update({server : player})

    @staticmethod
    def remove(server: str) -> None:
        del Servers.dict[str(server)]
