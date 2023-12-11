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
    """Tracks the computer players in the game.

        Attributes:
        name(str): the computer player's name. 
        hand (lst): the personal hand of cards
    """
    
    def card_selection(self,match_pile,matched_cards):
        """Randomly selects a card from matched cards.
        
        Primary Author(s): Matthew Manik

        Args:
            match_pile (lst): pile from which the player matches the card on top
            matched_cards (lst): list of matched cards from the player's personal hand
            
        Side effects:
            Writes to stdout.
        """
        
        # Out of the player's matched cards, computer randomly chooses a card to play.
        match_pile[-1]
        if len(matched_cards)>=1:
            position = random.randint(0, len(matched_cards)-1)
            card_position = int(position)
            print(f"{self.name}'s turn to choose a card")
            print(f"\nTo match the card: {match_pile[-1]}, the card {self.name} "
                  f"selected is {matched_cards[card_position]}\n")

            match_pile.append(matched_cards[card_position])
            if matched_cards[card_position] in self.hand:
                self.hand.remove(matched_cards[card_position])
        elif len(matched_cards) == 0:
            print("Error: Matched Cards is 0")

class Game:
    """Uno Game: Defense Editon. 
    
    Attributes:
    players (lst): list of HumanPlayer and ComputerPlayer instances
    deck (lst): original standard deck of cards
    draw_pile (list): deck of cards from which the player draws cards from. 
    gamemaster (bool, optional): allows user to see or not to see the 
                                 player's hand during the game. Defaults to False.
    next_player (int, optional): position of the next player according to the player list
    clockwise (int, optional): direction of the game. Defaults to 1.
    """
    
    def __init__(self, player_list, deck,gamemaster=False, next_player = 0, clockwise = 1):
        """Creates a single gamestate.

        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik
        
        Args:
            players (lst): list of HumanPlayer and ComputerPlayer instances
            deck (lst): original standard deck of cards
            draw_pile (list, optional): deck of cards from which the player draws cards from. Defaults to [].
            match_pile (list, optional): deck of cards which players have matched. Defaults to [].
            gamemaster (bool, optional): allows user to see or not to see the 
                                         player's hand during the game. Defaults to False.
        """
        self.player_list = player_list
        self.deck = deck
        self.draw_pile = deck.copy()
        self.gamemaster = gamemaster
        self.next_player = next_player
        self.clockwise = clockwise

    def setting_up(self):
        """Setting up Uno game.
        
        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik

        Args:
            player_list (lst): list of HumanPlayer and ComputerPlayers
            draw_pile (lst): deck of cards from which the player draws cards from
            match_pile (lst): deck of cards which players have matched
            
        Side effects:
            Writes to stdout.
        """
        # Shuffle the deck
        match_pile = []
        random.shuffle(self.deck)
        print("----- This is the start of UNO! -----\n")
        
        # Ask user if they want to see the other player's hands for debugging purposes
        while True:
            try:
                oversee_game = input("Would you like to see the player's hand during the game? (y/n)")
                if oversee_game == "y":
                    self.gamemaster = True
                    break
                elif oversee_game == "n":
                    self.gamemaster = False
                    break
                else:
                    print(f"\nChoose either yes or no (y/n)")
            except ValueError:
                print("\nError: Invalid")
        
        if self.gamemaster == True:
            print("\nYou chose to oversee the game and see the other players' hands!\n")
        elif self.gamemaster == False:
            print("\nYou chose not to see the other players' hands during the game!\n")
        
        # Distribute cards to players
        print(f"\nStarting in clockwise, the order of players are:")
        order = 0
        for player in self.player_list:
            order +=1
            print(f"{order}. {player.name}")
            for _ in range(7):
                card = self.deck.pop()
                player.hand.append(card)

        for player in self.player_list:
            if self.player_list.index(player) == 0:
                print(f"\n{player.name}, you are dealt 7 cards")
            else:
                print(f"{player.name} is dealt 7 cards")
            
        # First card to match cannot be a special card
        for card in self.deck:
            if (card["Type"]!="Special"):
                match_pile.append(card)
                break
            else:
                continue
        
        match_pile.append(card)
        return match_pile
    
    def reverse(self,player,match_pile):
        """Reverses the direction of the game.
        
        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik

        Args:
            player (class_instance): player of the game
            player_list (lst): list of HumanPlayer and ComputerPlayers
            match_pile (lst): deck of cards which players have matched

        Returns:
            match_pile (lst): deck of cards which players have matched
            player (class_instance): player of the game
            
        Side effects:
            Writes to stdout.
        """
        shield = 0
        print(f"{player.name} played a Reverse!")
        
        # Set the player to receive the Reverse
        position = (self.next_player + self.clockwise) % len(self.player_list)
        player = self.player_list[position]
        
        for card in player.hand:
            # If the receiving player has the Shield in their hand, they can block the Reverse.
            if card["Function"]=="Shield":
                    print(f"{player.name} plays the Shield and blocked the Reverse!")
                    match_pile.append(card)
                    player.hand.remove(card)
                    shield += 1
                    player = self.player_list[self.next_player]

                    # The Shield maintains the current direction of the game.
                    if self.clockwise == 1:
                        print(f"The direction remains Clockwise")
                    elif self.clockwise != 1:
                        print(f"The direction remains Counter-Clockwise")
                    break
            else:
                continue
        
        # If the receiving player player doesn't have the Shield, then the Reverse goes as normal
        if shield == 0:
            self.clockwise *= -1  
        return match_pile, player

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
    
    def skip(self,player,match_pile):
        """Skips the next player's turn.
        
        Primary Author(s): William Delmo, Vinhan Ky, Matthew Manik

        Args:
            player (class_instance): player of the game
            match_pile (lst): deck of cards which players have matched

        Returns:
            match_pile (lst): deck of cards which players have matched
            player (class_instance): player of the game
            
        Side effects:
            Writes to stdout.
        """
        
        # Set player to receive the Skip
        print(f"----- {player.name} played a Skip! -----")
        shield = 0
        position = (self.next_player + self.clockwise) % len(self.player_list)
        player = self.player_list[position]
        
        for card in player.hand:
            # If the receiving player has the Shield in their hand, they can block the Skip.
            if card["Function"]=="Shield":
                print(f"{player.name} plays the Shield and blocked the Skip!")
                match_pile.append(card)
                player.hand.remove(card)
                shield += 1
                print(f"It remains {player.name}'s turn!")
                break
            else:
                continue
        
        # If the receiving player player doesn't have the Shield, then they are skipped
        if shield == 0:
            self.next_player = (self.next_player + self.clockwise) % len(self.player_list)
            print(f"----- {self.player_list[self.next_player].name}'s turn was skipped! -----\n")
        
        return match_pile, player
      
                
    def turn(self,player,cards_added,matched_cards,match_pile,count):
        """A player's turn.
        
        Primary Author(s): Matthew Manik
        Techniques used: Sequence Unpacking

        Args:
            player (class_instance): player of the game
            cards_added (int): number of cards added to the list
            matched_cards (lst): list of matched cards from the player's personal hand
            match_pile (lst): deck of cards which players have matched
            draw_pile (lst): deck of cards from which the player draws cards from.
            count (int): Number of turns

        Returns:
            match_pile (lst): deck of cards which players have matched
            player (class_instance): player of the game
        
        Side effects:
            Writes to stdout.
        """
        if self.clockwise == 1:
            print(f"\nTurn #{count} --- Clockwise")
        elif self.clockwise != 1:
            print(f"\nTurn #{count} --- Counter-Clockwise")
        
        print(f"\n----- {player.name}'s turn -----\n")
        print(f"----- {player.name} has {len(player.hand)} cards -----\n")
        
        # Player checks hand for match
        match_in_hand = player.checking_hand(match_pile, self.draw_pile)
        
        if self.gamemaster == True:
            print(player)
        elif self.gamemaster == False:
            if self.player_list.index(player) == 0:
                print(player)
        
        # Player can draw to find a matched card
        matched_cards, cards_added = player.draw_to_match(match_in_hand, match_pile, self.draw_pile)
        
        if (len(matched_cards) != 0) and (self.player_list.index(player) == 0):
            print(f"{player.name} found {len(matched_cards)} matches in their hand.\n")
        
        if cards_added != 0:
            print(f"{player.name} drew {cards_added} more cards.\n")
        
        if self.player_list.index(player) == 0:
            if len(matched_cards) == 1:
                print(f"{player.name}'s matched card is {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
            elif len(matched_cards) > 1:
                print(f"{player.name}'s matched cards are {json.dumps(matched_cards, sort_keys=False, indent=4)}\n")
        
        # Player selects a card from their list of matched cards
        player.card_selection(match_pile,matched_cards)
        
        # Print player's hand using str method
        if self.player_list.index(player) == 0:
            print(player)
                
        return match_pile, player

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