from discord.voice_client import VoiceClient

# imports for classes from other files
import Queue
import Song


class Server_Dict():
    def __init__(self):
        self.dict = {}

    # idk what type player is
    def add(self, server: str | int, queue: Queue, vc: VoiceClient,) -> None:
        self.dict[str(server)] = {"queue": queue, "vc": vc,
                                  "player": None, "current_song": None,
                                  "loop": False, "queue_loop": False,
                                  "player_is_running": False}

    def remove(self, server: str) -> None:
        del self.dict[str(server)]

    def get_queue(self, server: str) -> Queue:
        return self.dict[str(server)]["queue"]

    def get_vc(self, server: str | int) -> VoiceClient:
        return self.dict[str(server)]["vc"]

    def get_player(self, server: str | int):  # idk what type player is
        return self.dict[str(server)]["player"]

    def set_player(self, server: str | int, player):  # idk what type player is
        self.dict[str(server)]["player"] = player

    def get_song(self, server: str | int, index: int) -> Song:
        return self.dict[str(server)].get(index)

    def get_current_song(self, server: str | int) -> Song:
        return self.dict[str(server)]["current_song"]

    def set_current_song(self, server: str | int, song: Song) -> None:
        self.dict[str(server)]["current_song"] = song

    def get_loop(self, server: str | int) -> bool:
        return self.dict[str(server)]["loop"]

    def set_loop(self, server: str | int, loop: bool) -> None:
        self.dict[str(server)]["loop"] = loop

    def get_queue_loop(self, server: str | int) -> bool:
        return self.dict[str(server)]["queue_loop"]

    def set_queue_loop(self, server: str | int, queue_loop: bool) -> None:
        self.dict[str(server)]["queue_loop"] = queue_loop

    def get_player_is_running(self, server: str | int) -> bool:
        return self.dict[str(server)]["player_is_running"]

    def set_player_is_running(self, server: str | int, player_is_running: bool) -> None:
        self.dict[str(server)]["player_is_running"] = player_is_running

    def get_all_songs(self, server: str | int) -> list:
        return self.dict[str(server)].get()

    def get_all_queues(self) -> list:
        return self.dict.values()

    def get_all_servers(self) -> list:
        return self.dict.keys()


if __name__ == "__main__":
    dict = Server_Dict()
    dict.add('server1', Queue.Queue())
    dict.add('server2', Queue.Queue())
    dict.add('server3', Queue.Queue())
    dict.add('server4', Queue.Queue())
    print(dict.get_all_songs_all_queues())
