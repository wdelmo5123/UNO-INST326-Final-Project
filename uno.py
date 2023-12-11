"""A game of Uno against the computer."""
import json
import random
from argparse import ArgumentParser
import sys

# List of cards
f = open('cards.json')
deck = json.load(f)

class HumanPlayer:
    """Tracks the human player throughout the game of Uno.

    Attributes:
        name(str): the player's name. 
        hand (lst): the personal hand
    """
    
    def __init__(self,name, hand=None):
        """Initialize Player Object of name and hand.
        
        Primary Author(s): William Delmo

        Args:
            name (str): name of Player
            hand (list): list of dictionaries (cards) the player has
        """
        
        self.name = name
        self.hand = hand if hand is not None else []

    def __str__(self):
        """Displays the player's name and hand in the game of UNO.
        
        Primary Author(s): William Delmo
        Techniques used: Magic Methods

        Returns:
            str: the player's name and hand of cards
        """
        if len(self.hand) == 0:
            return f"Length of {self.name}'s hand is 0"
        else:
            return f"{self.name}'s hand is {json.dumps(self.hand, sort_keys=False, indent=4)}"
        
    def checking_hand(self,match_pile,draw_pile):
        """Checking cards in personal hand for a match.
        
        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik

        Args:
            match_pile (lst): pile from which the player matches the card on top
            draw_pile (lst): deck of cards from which the player draws cards from.

        Returns:
            lst: list of matched cards from the player's personal hand
            
        Side effects:
            Writes to stdout.
        """
        
        matched_cards = []
        shield_amt = 0
        print(f"\nCard to match is {match_pile[-1]}\n")
        
        # Checking for matched cards from personal hand
        # Making sure a player only has one Shield in their hand
        if match_pile[-1]["Function"] != "Shield":
            print(f"{self.name} is checking each card in hand to see if it"
                  f" matches the card on table\n")
            for card in self.hand:
                if card["Color"] == match_pile[-1]["Color"]:
                    if (card["Function"]== "Shield"):
                        shield_amt += 1  
                    else:
                        matched_cards.append(card)
                elif card["Number"] == match_pile[-1]["Number"]:
                    if (card["Function"]== "Shield"):
                        shield_amt += 1   
                    else:    
                        matched_cards.append(card)  
                elif (card["Function"]== "Shield"):
                    shield_amt += 1                                                 
                else:
                    continue     
            for card in self.hand:
                if (card["Function"]== "Shield") and (shield_amt>=2):
                    self.hand.remove(card)
                    self.hand.append(draw_pile.pop())
            for card in matched_cards:
                if card["Function"]== "Shield":
                    matched_cards.remove(card)
                else:
                    continue
        # When Shield is played, you can put down other color cards, exceptions apply.
        elif match_pile[-1]["Function"] == "Shield":
            print(f"Since {self.name} played the Shield, {self.name} can put"
                  f" down any color card for others to match. However, these"
                f" exclude putting down Skips, Reverses, or Plus Twos.\n")
            for card in self.hand:
                if (card["Type"]!="Special"):
                    matched_cards.append(card)
            
            # If only special cards on hand, the next color card in draw pile is the card to match
            if len(matched_cards) == 0:
                print(f"{self.name} did not find any special cards.\n")
                for card in draw_pile:
                    for card in self.deck:
                        if (card["Type"]!="Special"):
                            match_pile.append(card)
                            break
                        else:
                            continue

        return matched_cards
           
    def draw_to_match(self,matched_cards,match_pile,draw_pile):
        """Drawing cards if the player has no match in their hand.
        
        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik

        Args:
            matched_cards (lst): list of matched cards from the player's personal hand
            match_pile (lst): pile from which the player matches the card on top
            draw_pile (lst): deck of cards from which the player draws cards from.

        Returns:
            matched_cards(lst): list of matched cards from the player's personal hand 
            cards_added(int): amount of cards the user added to their hand from the draw pile
            
        Side effects:
            Writes to stdout.
        """
        cards_added = 0
        shield_drawn = 0
        
        # If user doesn't have any matched cards, 
        # they have to draw from the draw pile until they find a match.
        if len(matched_cards) == 0:
            print(f"Cards in hand do not match, {self.name}'s drawing more cards")  
            for card in draw_pile:
                if card["Color"] == match_pile[-1]["Color"]:
                    matched_cards.append(card)
                    cards_added+=1
                    break
                elif card["Number"] == match_pile[-1]["Number"]:
                    matched_cards.append(card)  
                    cards_added+=1
                    break
                # Only allow player to draw one Shield
                elif (card["Function"]== "Shield"):
                    if shield_drawn > 0:
                        continue
                    elif shield_drawn == 0:
                        shield_drawn+=1
                        self.hand.append(card)
                else:
                    self.hand.append(card)
                    cards_added+=1
        return matched_cards, cards_added

    def card_selection(self,match_pile, matched_cards):
        """Select a card from the player's matched cards.
        
        Primary author(s): Matthew Manik
        Techniques used: json.dumps

        Args:
            match_pile (lst): pile from which the player matches the card on top
            matched_cards (lst): list of matched cards from the player's personal hand
            
        Side effects:
            Writes to stdout.
        """
        card_position = 0
        match_pile[-1]
        
        # Out of the player's matched cards, ask human player to play one card.
        if len(matched_cards)>=1:
            while True:
                try:
                    position = int(input(f"\nWhich card do you want to play?"
                                         f" From matched cards, select card position:"))
                    if 0 <= position < (len(matched_cards)):
                        break
                    else:
                        print(f"\nError: Choose a number between 0 and {len(matched_cards)-1}")
                except ValueError:
                    print("\nError: This is not an integer. Try again...")
            card_position = position
            print(f"\n----- {self.name} chooses a card -----")
            print(f"\nTo match the card: \n"
                  f"{json.dumps(match_pile[-1], sort_keys=False, indent=4)}, \n")
            print(f"the card selected is \n\n"
                  f"{json.dumps(matched_cards[card_position], sort_keys=False, indent=4)}\n\n")
            match_pile.append(matched_cards[card_position])  
            if matched_cards[card_position] in self.hand:
                self.hand.remove(matched_cards[card_position]) 
        
    def plus_two(self,match_pile, draw_pile):
        """Creating list of two cards to be added to opponent.

        Primary Author(s): William Delmo
        Techniques used: f string
        
        Args:
            match_pile (lst): pile from which the player matches the card on top
            draw_pile (lst): deck of cards from which the player draws cards from.

        Returns:
            draw_two(lst): list of two cards from draw pile
            
        Side effects:
            Writes to stdout.
        """
        # Create a list of two cards for player to receive
        draw_two = []
        if match_pile[-1]["Function"] == "+2":
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

    def drawing_two(self,player,match_pile):
        """Drawing two cards for next player in the game of UNO.
        
        Primary Author(s): William Delmo

        Args:
            player (class_instance): player of the game
            match_pile (lst): deck of cards which players have matched
            draw_pile (lst): deck of cards from which the player draws cards from

        Returns:
            match_pile (lst): deck of cards which players have matched
            player (class_instance): player of the game
            
        Side effects:
            Writes to stdout.
        """
        # Set player to receive the two cards
        draw_two = player.plus_two(match_pile, self.draw_pile)
        shield = 0
        position = (self.next_player + self.clockwise) % len(self.player_list)
        player = self.player_list[position]
        
        for card in player.hand:
            # If the receiving player has the Shield in their hand, they can block the Reverse.
            if card["Function"]=="Shield":
                print(f"{player.name} plays the Shield and reflects the +2!")
                match_pile.append(card)
                player.hand.remove(card)
                shield += 1
                player = self.player_list[self.next_player]
                print(f"{player.name} now has to draw 2 cards!")
                player.hand.extend(draw_two)
                break
            else:
                continue
        
        # If the receiving player player doesn't have the Shield, then they draw two
        if shield == 0:
            player.hand.extend(draw_two)
            print(f"----- {player.name} draws 2 more cards -----\n")  
        
        return match_pile, player
    
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