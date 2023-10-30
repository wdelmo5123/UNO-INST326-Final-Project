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
    