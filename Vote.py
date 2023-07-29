from discord import Member


class Vote:
    """
    A class for keeping track of users who have voted to do x

    Attributes
    ----------
    initiator : discord.Member
        The Member who initiated the Vote.
    voters :  list[discord.Member]
        A list of all members who have voted, from first to last.    

    Methods
    -------
    add(member: discord.Member)
        Adds a Member to the list of voters.
    get()
        Returns the list of voters
    """
    def __init__(self, initiator: Member):
        """
        Parameters
        ----------
        initiator : discord.Member
            The Member who initiated the Vote.
        """
        self.initiator = initiator
        self.voters = [initiator]

    def __len__(self) -> int:
        return len(self.voters)

    def add(self, member: Member) -> None:
        """
        Parameters
        ----------
        member : discord.Member
            The Member to be added to the list of voters.
        """
        self.voters.append(member)
        return

    def get(self) -> list[Member]:
        """
        Returns
        -------
        list[discord.Member]:
            A list of all members who have voted, from first to last.
        """
        return self.voters
