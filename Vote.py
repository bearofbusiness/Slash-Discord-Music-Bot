from Song import Song
from discord import Member
class Vote:
    def __init__(self, song: Song, initiator: Member):
        self.song = song
        self.initiator = initiator
        self.voters = [initiator]

    def __len__(self) -> int:
        return len(self.voters)

    def add(self, member: Member) -> None:
        self.voters.append(member)
        return
    
    def get(self) -> list:
        return self.voters
