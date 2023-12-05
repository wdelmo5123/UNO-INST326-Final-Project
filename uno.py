"""A game of Uno against the computer."""
import json
import random
from argparse import ArgumentParser
import sys

# List of cards
f = open('cards.json')
deck = json.load(f)

class HumanPlayer:
    """Tracks the names of the player in Uno.

        Attributes:
        name(str): the player's name. 
        hand (lst): the personal hand
        hand_amt (int): amount of cards the player has
    """
    
    def __init__(self,name, hand=None):
        """ Initialize Player Object

        Args:
            name (str): name of Player
            hand (list): list of dictionaries (cards) the player has
            hand_amt (int): amount of cards the player has
        """
        
        self.name = name
        self.hand = hand if hand is not None else []
        
    def cardchoice(self,match_pile,draw_pile):
        """ 
        
        Args:
            state (str): Visual Output to print the card on the table,
            the amount of cards other people have. 
            
        Returns:
            card (dict): A matched card that will be appended to the matched pile
        """
        # One Turn
        # Player selects card to match card on table
        
        
        if len(self.hand) == 1:
            # Play the only available card in the hand
            card = self.hand[0]
            match_pile.append(card)  
            if card in self.hand:
                self.hand.remove(card)
    
        while len(self.hand) > 0:

            c = "Color"
            n = "Number"
            count = 0
            card_position = 0
            cards_added = 0

            # Take card on top of table to match
            
            # Starting game, so we do not want to pop, bc theres only one card in match pile
            card_on_table = match_pile[-1]

            
            
            
            print(f"Card is {card_on_table}\n")

            # List of matched cards
            matched_cards = []
            
            # Checks each card in personal hand if it matches card on table
            print(f"Card to match is {card_on_table}\n")
                
                
            print(f"Checking each card in hand to see if it matches the card on table\n")
            for card1 in self.hand:
                if card1[c] == card_on_table[c]:
                    print(f"Found Color Match for color {card1[c]}\n")
                    matched_cards.append(card1)
                elif card1[n] == card_on_table[n]:
                    print(f"Found Match for number {card1[n]}\n")
                    matched_cards.append(card1)                                                         
                else:
                    print(f"Card does not match in color or number\n")

           
            print(f"Cards in hand do not match, so draw cards\n")
            # When cards in personal hand do not match, cards are drawn to match
            if len(matched_cards) == 0:
                print(f"Currently drawing more cards")  
                for card1 in draw_pile:
                    if card1[c] == card_on_table[c]:
                        print(f"Found Color Match for color {card1[c]}")
                        matched_cards.append(card1)
                        cards_added+=1
                        break
                    elif card1[n] == card_on_table[n]:
                        print(f"Found Match for number {card1[n]}")
                        matched_cards.append(card1)   
                        cards_added+=1
                        break
                    else:
                        print(f"Card drawn is not a match. Adding to Personal Hand... ")
                        self.hand.append(card1)
                        cards_added+=1

            print(f"\nPersonal Hand is now {json.dumps(self.hand, sort_keys=False, indent=4)}\n")
            print(f"\nYour Personal hand has {len(self.hand)} cards\n")
            print(f"You drew {json.dumps(cards_added, sort_keys=False, indent=4)} more cards to your personal hand\n")

            # Printing the player's matched cards
            if len(matched_cards) == 1:
                print(f"Your matched card is {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
            elif len(matched_cards) > 1:
                print(f"Your matched cards are {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")

            # Selecting a card from matched cards to play
            while matched_cards and count < 1 and (0 <= card_position <= len(matched_cards)):
                count+=1
                position = input(f"Which card do you want to play? From matched cards, select card position:")
                card_position = int(position)
                while card_position > (len(matched_cards)):
                    position = input(f"Please select a card position less than or equal to {len(matched_cards)}:")
                    card_position = int(position)
                print(f"\nTo match the card: {card_on_table}, the card selected is {matched_cards[card_position]}")
                match_pile.append(matched_cards[card_position])  
                if matched_cards[card_position] in self.hand:
                    self.hand.remove(matched_cards[card_position])
                return matched_cards[card_position]
    
    def plus_two(self, draw_pile, match_pile):
        table = match_pile[-1]
        for card in self.hand:
            if card["Color"] == table["Color"]:
                match_pile.append(card)
                for card in match_pile:
                    if card["Function"] == "+2":
                        print(f"person adds two cards!")
                        if len(draw_pile) > 0:
                            card = draw_pile.pop()
                            self.hand.append(card)
                            card = draw_pile.pop()
                            self.hand.append(card)
                        else:
                            print(f"Draw pile is empty!")
                    else: 
                        print(f"This card doesn't add two!")
            elif card["Function"] == table["Function"]:
                match_pile.append(card)
                for card in match_pile:
                    if card["Function"] == "+2":
                        print(f"person adds two cards!")
                        if len(draw_pile) > 0:
                            card = draw_pile.pop()
                            self.hand.append(card)
                            card = draw_pile.pop()
                            self.hand.append(card)
                        else:
                            print(f"Draw pile is empty!")
                    else: 
                        print(f"This card doesn't add two!")  
            
        
class ComputerPlayer:
    """Tracks the names of the player in Uno.

        Attributes:
        name(str): the player's name. 
        hand (lst): the personal hand
        hand_amt (int): amount of cards the player has
    """
    
    def __init__(self,name, hand=None):
        """ Initialize Player Object

        Args:
            name (str): name of Player
            hand (list): list of dictionaries (cards) the player has
            hand_amt (int): amount of cards the player has
        """
        
        self.name = name
        self.hand = hand if hand is not None else []
        
    def cardchoice(self,match_pile,draw_pile):
        """ 
        
        Args:
            state (str): Visual Output to print the card on the table,
            the amount of cards other people have. 
            
        Returns:
            card (dict): A matched card that will be appended to the matched pile
        """
        # One Turn
        # Player selects card to match card on table
        
        
        if len(self.hand) == 1:
            # Play the only available card in the hand
            card = self.hand[0]
            match_pile.append(card)  
            if card in self.hand:
                self.hand.remove(card)
    
        while len(self.hand) > 0:

            c = "Color"
            n = "Number"
            count = 0
            card_position = 0
            cards_added = 0

            # Take card on top of table to match
            
            # Starting game, so we do not want to pop, bc theres only one card in match pile
            card_on_table = match_pile[-1]
            
            
            
            print(f"Card is {card_on_table}\n")

            # List of matched cards
            matched_cards = []
            
            # Checks each card in personal hand if it matches card on table
            print(f"Card to match is {card_on_table}\n")
                
                
            print(f"Checking each card in hand to see if it matches the card on table\n")
            for card1 in self.hand:
                if card1[c] == card_on_table[c]:
                    print(f"Found Color Match for color {card1[c]}\n")
                    matched_cards.append(card1)
                elif card1[n] == card_on_table[n]:
                    print(f"Found Match for number {card1[n]}\n")
                    matched_cards.append(card1)                                                         
                else:
                    print(f"Card does not match in color or number\n")

           
            print(f"Cards in hand do not match, so draw cards\n")
            # When cards in personal hand do not match, cards are drawn to match
            if len(matched_cards) == 0:
                print(f"Currently drawing more cards")  
                for card1 in draw_pile:
                    if card1[c] == card_on_table[c]:
                        print(f"Found Color Match for color {card1[c]}")
                        matched_cards.append(card1)
                        cards_added+=1
                        break
                    elif card1[n] == card_on_table[n]:
                        print(f"Found Match for number {card1[n]}")
                        matched_cards.append(card1)   
                        cards_added+=1
                        break
                    else:
                        print(f"Card drawn is not a match. Adding to Personal Hand... ")
                        self.hand.append(card1)
                        cards_added+=1

            print(f"\nPersonal Hand is now {json.dumps(self.hand, sort_keys=False, indent=4)}\n")
            print(f"\nYour Personal hand has {len(self.hand)} cards\n")
            print(f"You drew {json.dumps(cards_added, sort_keys=False, indent=4)} more cards to your personal hand\n")

            # Printing the player's matched cards
            if len(matched_cards) == 1:
                print(f"Your matched card is {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
            elif len(matched_cards) > 1:
                print(f"Your matched cards are {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")

            # Selecting a card from matched cards to play
            while matched_cards and count < 1 and (0 <= card_position <= len(matched_cards)):
                count+=1
                while card_position > (len(matched_cards)):
                    print(f"Which card do you want to play? From matched cards, select card position:")
                    position = random.randint(0, len(matched_cards))
                    card_position = int(position)
                print(f"\nTo match the card: {card_on_table}, the card selected is {matched_cards[card_position]}")
                match_pile.append(matched_cards[card_position])
                if matched_cards[card_position] in self.hand:
                    self.hand.remove(matched_cards[card_position])
                
                return matched_cards[card_position]
    
    def plus_two(self, draw_pile, match_pile):
        table = match_pile[-1]
        for card in self.hand:
            if card["Color"] == table["Color"]:
                match_pile.append(card)
                for card in match_pile:
                    if card["Function"] == "+2":
                        print(f"person adds two cards!")
                        if len(draw_pile) > 0:
                            card = draw_pile.pop()
                            self.hand.append(card)
                            card = draw_pile.pop()
                            self.hand.append(card)
                        else:
                            print(f"Draw pile is empty!")
                    else: 
                        print(f"This card doesn't add two!")
            elif card["Function"] == table["Function"]:
                match_pile.append(card)
                for card in match_pile:
                    if card["Function"] == "+2":
                        print(f"person adds two cards!")
                        if len(draw_pile) > 0:
                            card = draw_pile.pop()
                            self.hand.append(card)
                            card = draw_pile.pop()
                            self.hand.append(card)
                        else:
                            print(f"Draw pile is empty!")
                    else: 
                        print(f"This card doesn't add two!")  



class Game:
    """Provide information on the current state of the game. Used in the
    Player.card_choice() method.
    
    Attributes:
    draw_pile(lst): deck of cards from which the player draws cards from
    match_pile(lst): deck of cards which players have matched
    hand_amt (int): amount of cards the player has
    
    """
    
    def __init__(self, players, deck, card = {}, draw_pile = [], match_pile=[], direction = "Clockwise"):
        self.players = players
        self.deck = deck
        self.card = card
        self.draw_pile = draw_pile
        self.match_pile = match_pile
        self.direction = direction
        
    # Initializing hand
    def distribute_cards(self, player_list, deck):
        
        random.shuffle(deck)
        count = 0
        for player in player_list:
            for _ in range(6):
                count += 1
                card = deck.pop()
                player.hand.append(card)


    
    # Purpose of this method is to allow the human and computer player
    # to play together until a player has no cards left
    def tournament(self, player_list,draw_pile, match_pile, direction):
        
        card = deck.pop() 
        match_pile.append(card)
        draw_pile = deck.copy()
     
        count = 0
        while count >= 0:
            for player in player_list:
                count+=1
                if player:
                    if len(player.hand)>= 1:
                        print(f"Round {count}\n")
                        print(f"\n{player.name}'s turn\n")
                        player.cardchoice(match_pile, draw_pile)
                        if len(player.hand) == 0:
                            count = -1
                            print(f"{player.name} wins!")
                            break

def main(filepath):
    """ Set up and play a game of uno.

    Args:
        filepath (str): path to the JSON file containing the uno cards.
        """

    with open(filepath, "r", encoding = "utf-8") as f:
            deck = json.load(f)

    human_player = HumanPlayer(name= "Steven")
    computer_player = ComputerPlayer(name= "Computer")

    game = Game(players = [human_player, computer_player], deck = deck, direction = "Clockwise")
    # Initialize the players' hands
    game.distribute_cards(player_list=[human_player, computer_player], deck=deck)

    # Play the tournament
    game.tournament(player_list=[human_player, computer_player], draw_pile=deck.copy(), match_pile=[], direction = "Clockwise")

def parse_args(arglist):
    """ Parse command-line arguments.

    Args:
        arglist (list of str): arguments from the command line

    Returns:
        namespace: the parsed arguments as a namespace.  
    """
    parser = ArgumentParser(description = "A game of uno against the computer")
    parser.add_argument("players", type = int, default = 2, help = "Number of players in the game (default: 2)")
    parser.add_argument("deck", type = str, default = "cards.json", 
                        help = "Path to JSON file containig the UNO card deck (default: card.json)")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.deck) 