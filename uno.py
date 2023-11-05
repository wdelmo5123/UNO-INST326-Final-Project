"""A game of Uno against the computer."""

class Player:
    """Tracks the names of the player in Uno.

        Attributes:
        name(str): the player's name. 
    """
    
    def __init__(self,name):
        """ Initialize Player Object

        Args:
            name (_str): name of Player
        """
        
        self.name = name

class ComputerPlayer:
    """The computer as a player.
    
    Attributes:
        names(str): the player's name.
        cards(str or list): the lists of cards that the computer will get cards from.
    """
    def __init__(self,computer):
        """ Initialize Player Object

        Args:
            name (_str): name of Player
        """
        
        self.computer = computer

class GameState:
    
    def __init__(self, player, card, hand, clockwise):
        self.player = player
        self.card = card
        self.hand = hand
        self.clockwise = clockwise
        self.clockwise = True
        
    def skip_turn(self):
        if self.card == "Skip":
            self.player[i] += 1 
            return print(f"{self.name} has been skipped!")
        
    def reverse_turn(self):
        if self.card == "Reverse":
            self.clockwise = False
            return print(f"{self.name} has used a reverse card!")