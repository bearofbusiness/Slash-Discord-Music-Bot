# imports for classes from other files
from Player import Player

class Servers():
    def __init__(self):
        self.dict = {}

    def add(self, server: str | int, player: Player) -> None:
        self.dict[str(server)] = player

    def get_player(self, server: str | int) -> Player:
        return self.dict.get(str(server))

    def set_player(self, server: str | int, player: Player):
        self.dict.update({server : player})

    def remove(self, server: str) -> None:
        del self.dict[str(server)]
