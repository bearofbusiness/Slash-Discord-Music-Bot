# imports for classes from other files
from Player import Player
from Vote import Vote


class Servers():
    def __init__(self):
        self.dict = {}

    def add(self, server: str | int, player: Player) -> None:
        self.dict[str(server)] = {
            "player": player,
            "skip_vote": None
        }

    def get_player(self, server: str | int) -> Player:
        return self.dict.get(str(server)).get("player")

    def set_player(self, server: str | int, player: Player):
        self.dict.get(server).update({"player": player})

    def get_skip_vote(self, server: str | int) -> Vote:
        return self.dict.get(str(server)).get("skip_vote")

    def set_skip_vote(self, server: str | int, vote: Vote):
        self.dict.get(server).update({"vote": vote})

    def remove(self, server: str) -> None:
        del self.dict[str(server)]
