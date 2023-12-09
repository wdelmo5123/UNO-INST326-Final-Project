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
    """
    
    def __init__(self,name, hand=None):
        """ Initialize Player Object

        Args:
            name (str): name of Player
            hand (list): list of dictionaries (cards) the player has
        """
        
        self.name = name
        self.hand = hand if hand is not None else []
    
    def __str__(self):
        if len(self.hand) == 0:
            return f"Length of {self.name}'s hand is 0"
        else:
            return f"{self.name}'s hand is {json.dumps(self.hand, sort_keys=False, indent=4)}"
        
    def cardchoice(self,match_pile,draw_pile):
        """ 
        
        Args:
            state (str): Visual Output to print the card on the table,
            the amount of cards other people have. 
            
        Returns:
            card (dict): A matched card that will be appended to the matched pile
        """
        

        c = "Color"
        n = "Number"
        cards_added = 0
        matched_cards = []
        
        card_on_table = match_pile[-1]
        print(f"\nCard to match is {card_on_table}\n")
            
            
        print(f"{self.name} is checking each card in hand to see if it matches the card on table\n")
        for card1 in self.hand:
            if card1[c] == card_on_table[c]:
                matched_cards.append(card1)
            elif card1[n] == card_on_table[n]:
                matched_cards.append(card1)                                                         
            else:
                continue
        
        
        # When cards in personal hand do not match, cards are drawn to match
        if len(matched_cards) == 0:
            print(f"Cards in hand do not match, {self.name}'s drawing more cards")  
            for card1 in draw_pile:
                if card1[c] == card_on_table[c]:
                    matched_cards.append(card1)
                    cards_added+=1
                    break
                elif card1[n] == card_on_table[n]:
                    matched_cards.append(card1)  
                    cards_added+=1
                    break
                else:
                    self.hand.append(card1)
                    cards_added+=1

        return matched_cards, cards_added

    def card_selection(self,match_pile, matched_cards):
        card_position = 0
        card_on_table = match_pile[-1]
        
        if len(matched_cards)>=1:
  
            while True:
                try:
                    position = int(input(f"\nWhich card do you want to play? From matched cards, select card position:"))
                    if 0 <= position < (len(matched_cards)):
                        break
                    else:
                        print(f"\nError: Choose a number between 0 and {len(matched_cards)-1}")
                except ValueError:
                    print("\nError: This is not an integer. Try again...")
        
            card_position = position
            print(f"\n----- {self.name} chooses a card -----")
            print(f"\nTo match the card: \n{json.dumps(card_on_table, sort_keys=False, indent=4)}, \n")
            print(f"the card selected is \n\n{json.dumps(matched_cards[card_position], sort_keys=False, indent=4)}\n\n")
            match_pile.append(matched_cards[card_position])  
            if matched_cards[card_position] in self.hand:
                self.hand.remove(matched_cards[card_position]) 
        
    def plus_two(self, draw_pile, match_pile):
        table = match_pile[-1]
        draw_two = []
        
        if table["Function"] == "+2":
            print(f"----- {self.name} plays a +2! -----")
            if len(draw_pile) > 0:
                card = draw_pile.pop()
                draw_two.append(card)
                card = draw_pile.pop()
                draw_two.append(card)
            else:
                print(f"Draw pile is empty!")
        else: 
            print(f"This card doesn't add two!") 
        
        return draw_two 
    
class ComputerPlayer(HumanPlayer):
    """Tracks the names of the player in Uno.

        Attributes:
        name(str): the player's name. 
        hand (lst): the personal hand
    """
    
    def card_selection(self,match_pile,matched_cards):
        card_on_table = match_pile[-1]
        
        if len(matched_cards)>=1:
            position = random.randint(0, len(matched_cards)-1)
            card_position = int(position)
            
            print(f"{self.name}'s turn to choose a card")
            # print(f"{self.name}'s hand is {json.dumps(self.hand, sort_keys=False, indent=4)}")
            # print(f"{self.name}'s matched_cards is {json.dumps(matched_cards, sort_keys=False, indent=4)}")
            
            print(f"\nTo match the card: {card_on_table}, {self.name} selected is {matched_cards}\n")
            
            match_pile.append(matched_cards[card_position])
            if matched_cards[card_position] in self.hand:
                self.hand.remove(matched_cards[card_position])
        elif len(matched_cards) == 0:
            print("why is len matched cards = 0?")
            
      

class Game:
    """Provide information on the current state of the game. Used in the
    Player.card_choice() method.
    
    Attributes:
    draw_pile(lst): deck of cards from which the player draws cards from
    match_pile(lst): deck of cards which players have matched
    hand_amt (int): amount of cards the player has
    
    """
    
    def __init__(self, players, deck, card = {}, draw_pile = [], match_pile=[]):
        self.players = players
        self.deck = deck
        self.card = card
        self.draw_pile = draw_pile
        self.match_pile = match_pile


    
    # Purpose of this method is to allow the human and computer player
    # to play together until a player has no cards left
    def tournament(self, player_list,draw_pile, match_pile):
        random.shuffle(deck)
        count = 0
        for player in player_list:
            for _ in range(7):
                card = deck.pop()
                player.hand.append(card)
                # print(f"{player.name} has {len(player.hand)} cards, and is adding a card")
        
        print("----- This is the start of UNO! -----\n")
        for player in player_list:
            if player_list.index(player) == 0:
                print(f"{player.name}, you are dealt 7 cards")
            else:
                print(f"{player.name} is dealt 7 cards")
        
            
        card = deck.pop() 
        match_pile.append(card)
        draw_pile = deck.copy()

        cards_added = 0
        count = 1
        next_player = 0
        clockwise = 1  
        matched_cards = []

        while count >= 1:
            
            if len(match_pile) == 10:
                for _ in range(8):
                    draw_pile.append(match_pile.pop(0))
                random.shuffle(draw_pile)
            
            
            player = player_list[next_player]
            
            if len(player.hand) == 1:
                # Play the only available card in the hand
                card = player.hand[0]
                match_pile.append(card)  
                if card in player.hand:
                    player.hand.remove(card)
                if len(player.hand) == 0:
                    if clockwise == 1:
                        print(f"\nTurn #{count} --- Clockwise")
                    elif clockwise != 1:
                        print(f"\nTurn #{count} --- Counter-Clockwise")
                    print(f"\n----- {player.name}'s turn -----")
                    print(f"\n----- {player.name}'s plays last card and wins!\n")
                    break
            
                    
            if len(player.hand)>= 1:
                if clockwise == 1:
                    print(f"\nTurn #{count} --- Clockwise")
                elif clockwise != 1:
                    print(f"\nTurn #{count} --- Counter-Clockwise")
                   
                    
                print(f"\n----- {player.name}'s turn -----\n")
                print(f"----- {player.name} has {len(player.hand)} cards -----\n")
                
                if player_list.index(player) == 0:
                    print(player)
                
                # Drawing Cards
                matched_cards, cards_added = player.cardchoice(match_pile, draw_pile)
                
                if (len(matched_cards) != 0) and (player_list.index(player) == 0):
                    print(f"{player.name} found {len(matched_cards)} matches in their hand.\n")
                
                if cards_added != 0:
                    print(f"{player.name} drew {cards_added} more cards.\n")
                
                # Printing the player's matched cards
                
                if player_list.index(player) == 0:
                    if len(matched_cards) == 1:
                        print(f"{player.name}'s matched card is {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
                    elif len(matched_cards) > 1:
                        print(f"{player.name}'s matched cards are {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
                    
                # Selecting Card
                player.card_selection(match_pile,matched_cards)
                
                if player_list.index(player) == 0:
                    print(player)

            
            if match_pile[-1]["Function"] == "Reverse":
                clockwise *= -1  
                
            if match_pile[-1]["Function"] == "+2":
                draw_two = player.plus_two(draw_pile, match_pile)
                
                if clockwise == 1:
                    
                    position = (next_player + clockwise) % len(player_list)
                    player = player_list[position]
                    player.hand.extend(draw_two)
                    print(f"----- {player.name} draws 2 more cards\n")  
                elif clockwise != 1:
                    position = (next_player + clockwise) % len(player_list)
                    player = player_list[position]
                    player.hand.extend(draw_two)
                    print(f"----- {player.name} draws 2 more cards\n")
                
            
            if match_pile[-1]["Function"]=="Skip":
                next_player = (next_player + clockwise) % len(player_list)
                print(f"----- {player.name} played a Skip! -----")
                print(f"----- {player_list[next_player].name}'s turn was skipped! -----\n")
                
            next_player = (next_player + clockwise) % len(player_list)
            
            count += 1

def main(player_list,deck):
    """ Set up and play a game of uno.

    Args:
        filepath (str): path to the JSON file containing the uno cards.
        """
    game = Game(player_list, deck = deck)

    game.tournament(player_list, draw_pile=deck.copy(), match_pile=[],)


def parse_args():
    parser = ArgumentParser(description="A game of Uno against the computer.")
    parser.add_argument("human_name", help="Name of the human player,only one human player")
    parser.add_argument("-c", "--computer_players", type=int, default=1,
                        help="Number of computer players")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

 
    player_list = [HumanPlayer(args.human_name)]

    name_list = ["Bob","Sally","David","Jean","Liz","Jack","Nate","George"]
    
    
    for i in range(args.computer_players):
        name = random.choice(name_list)
        computer_player = ComputerPlayer(f"{name}")
        name_list.remove(name) 
        player_list.append(computer_player)


    main(player_list, deck)  