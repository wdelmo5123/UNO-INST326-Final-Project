"""A game of Uno against the computer."""

class Player:
    """Tracks the names of the player in Uno.

        Attributes:
        name(str): the player's name. 
    """
    
    def __init__(self,name, hand):
        """ Initialize Player Object

        Args:
            name (str): name of Player
        """
        
        self.name = name
        self.hand = hand 

class ComputerPlayer:
    """The computer as a player.
    
    Attributes:
        names(str): the player's name.
        cards(str or list): the lists of cards that the computer will get cards from.
    """
    def __init__(self, name, hand):
        """ Initialize Player Object

        Args:
            name (str): name of Player
        """
        
        self.name = name
        self.hand = hand

class GameState:
    
    def __init__(self, player, card, hand):
        self.player = player
        self.card = card
        self.hand = hand
    