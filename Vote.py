from discord import Member


class Vote:
    def __init__(self, initiator: Member):
        self.initiator = initiator
        self.voters = [initiator]

    def __len__(self) -> int:
        return len(self.voters)

    def add(self, member: Member) -> None:
        self.voters.append(member)
        return

    def get(self) -> list[Member]:
        return self.voters
