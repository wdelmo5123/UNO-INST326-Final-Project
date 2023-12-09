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
                        #print(f"Found Match for number {card1[n]}")
                        matched_cards.append(card1)   
                        cards_added+=1
                        break
                    else:
                        print(f"Card drawn is not a match. Adding to Personal Hand... ")
                        self.hand.append(card1)
                        cards_added+=1

            
            # print(f"\nYour Personal hand has {len(self.hand)} cards\n")
            # print(f"You drew {json.dumps(cards_added, sort_keys=False, indent=4)} more cards to your personal hand\n")

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
                print(f"{self.name}'s turn")
                print(f"\nTo match the card: \n{json.dumps(card_on_table, sort_keys=False, indent=4)}, \nthe card selected is \n\n{json.dumps(matched_cards[card_position], sort_keys=False, indent=4)}\n\n")
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
                        print(f"{self.name} adds two cards!")
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
                        print(f"{self.name} adds two cards!")
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
        
        name_list = ["Bob","Sally","David","Jean","Liz","Jack","Nate","Mark"]
        self.name = random.choice(name_list)
        name_list.remove(self.name)  
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

          
            card_on_table = match_pile[-1]
            matched_cards = []
            
            for card1 in self.hand:
                if card1[c] == card_on_table[c]:
                    matched_cards.append(card1)
                elif card1[n] == card_on_table[n]:
                    matched_cards.append(card1)                                                         
                else:
                    print("")

           
            
            if len(matched_cards) == 0:
                
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

          
    
            while matched_cards and count < 1 and (0 <= card_position <= len(matched_cards)):
                count+=1
               
                while card_position > (len(matched_cards)):
                    
                    position = random.randint(0, len(matched_cards))
                    card_position = int(position)
                
                print(f"{self.name}'s turn")
                print(f"\nTo match the card: {card_on_table}, {self.name} selected {matched_cards[card_position]}\n")
                
                    
               
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
                        print(f"{self.name} adds two cards!")
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
                        print(f"{self.name} adds two cards!")
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
        print("This is the start of UNO!")
        for player in player_list:
            print(f"{player.name} is drawing cards")
            print(HumanPlayer(player.name, player.hand))
            
        card = deck.pop() 
        match_pile.append(card)
        draw_pile = deck.copy()


        count = 1
        next_player = 0
        clockwise = 1  

        while count >= 1:
            
            player = player_list[next_player]

            
            if len(player.hand)>= 1:
                print(f"Round {count}\n")
                print(f"\n{player.name}'s turn\n")
                print(f"{player.name} has {len(player.hand)} cards\n")
                print(HumanPlayer(player.name, player.hand))
                
                player.cardchoice(match_pile, draw_pile)
                print(f"{player.name} has taken a turn")
                print(HumanPlayer(player.name, player.hand))

                if len(player.hand) == 0:
                    print(f"{player.name} wins!")
                    break

            
            if match_pile[-1]["Function"] == "Reverse":
                clockwise *= -1  
            elif match_pile[-1]["Function"] == "+2":
                player.plus_two(draw_pile, match_pile)
                


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


    for i in range(args.computer_players):
        computer_player = ComputerPlayer(f"Computer_{i+1}")
        player_list.append(computer_player)



    main(player_list, deck)  