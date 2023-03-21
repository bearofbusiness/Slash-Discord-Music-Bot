

#imports for classes from other files
import Queue, Song
class ServerDict():
    def __init__(self):
        self.dict = {}

    def add(self, server: str, queue: Queue) -> None:
        self.dict[server] = queue

    def remove(self, server: str) -> None:
        del self.dict[server]

    def get(self, server: str) -> Queue:
        return self.dict[server]

    def get_all(self) -> dict:
        return self.dict
    
    def length(self) -> int:
        return len(self.dict)

    def get_queue(self, server: str) -> Queue:
        return self.dict[server]

    def get_song(self, server: str, index: int) -> Song:
        return self.dict[server].get()[index]

    def get_all_songs(self, server: str) -> list:
        return self.dict[server].get()

    def get_all_queues(self) -> list:
        return self.dict.values()

    def get_all_servers(self) -> list:
        return self.dict.keys()

    def get_all_songs_all_queues(self) -> list:
        return [f"{server}:{queue.get()}/n" for server, queue in self.dict.items()]
    
    
if __name__ == "__main__":
    dict = ServerDict()
    dict.add('server1', Queue.Queue())
    dict.add('server2', Queue.Queue())
    dict.add('server3', Queue.Queue())
    dict.add('server4', Queue.Queue())
    print(dict.get_all_songs_all_queues())
