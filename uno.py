"""A game of Uno against the computer."""
import json
import random

f = open('card_data.json')
table_cards = json.load(f)
drawing_cards = json.load(f)

# Shuffling both decks
random.shuffle(drawing_cards)
random.shuffle(table_cards)


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
    def __init__(self,computer, hand):
        """ Initialize Player Object

        Args:
            name (str): name of Player
        """
        
        self.computer = computer
        self.hand = hand

class Game:
    
    def __init__(self, player, card, hand):
        self.player = player
        self.card = card
        self.hand = hand
        
    def drawing_cards(self,drawing_cards,table_cards):
        """Drawing cards if player finds no match. 
        
           Ideally, you would have one deck of cards to 
           first shuffle through
           create the personal hand for players, 
           and the card on top would be the first card to match.
           
           Ideally, personal hand would also be an argument of the function.
           In this case, a personal hand is initialized.
           
           In this function, drawing_cards and table_cards are treated as
           separate decks.
           
           Technically, this function has the player play by themselves. 
           Where each round, the card on top of table_cards is the card to match.
           
            

        Args:
            drawing_cards (lst): list of cards to draw from 
            table_cards (lst): list of cards, where card on top is card to match
        """
        
        # Temporarily initializing a personal hand 
        personal_hand = [
          {"Type" : "Number",
          "Color" : "Blue",
          "Number" : 1,
          "Function" : "None"},
         
         {"Type" : "Number",
          "Color" : "Blue",
          "Number" : 1,
          "Function" : "None"},
         
         {"Type" : "Number",
          "Color" : "Blue",
          "Number" : 1,
          "Function" : "None"}
    
            ]
        
        game = 0
        while len(personal_hand) > 0:
            game+=1
            print(f"\nThis is Round #{game}")

            c = "Color"
            n = "Number"
            count = 0
            card_position = 0
            cards_added = 0

            # Take card on top of table to match
            card_on_table = table_cards.pop(0)
            print(f"Card is {card_on_table}\n")

            # List of matched cards
            matched_cards = []

            print(f"\nPersonal Hand is {personal_hand}\n")
            
            # Checks each card in personal hand if it matches card on table
            for card1 in personal_hand:
                if card1[c] == card_on_table[c]:
                    print(f"Found Color Match for color {card1[c]}\n")
                    matched_cards.append(card1)
                elif card1[n] == card_on_table[n]:
                    print(f"Found Match for number {card1[n]}\n")
                    matched_cards.append(card1)                                                         
                else:
                    print(f"Card does not match in color or number\n")

            print(f"Card to match is {card_on_table}\n")

            # When cards in personal hand do not match, cards are drawn to match
            if len(matched_cards) == 0:
                print(f"Currently drawing more cards")  
                for card1 in drawing_cards:
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
                        personal_hand.append(card1)
                        cards_added+=1

            print(f"\nPersonal Hand is now {personal_hand}\n")
            print(f"\nYour Personal hand has {len(personal_hand)} cards\n")
            print(f"You drew {cards_added} more cards to your personal hand\n")

            # Printing the player's matched cards
            if len(matched_cards) == 1:
                print(f"Your matched card is {matched_cards}\n")
            elif len(matched_cards) > 1:
                print(f"Your matched cards are {matched_cards}\n")
            
            print(f"Card to match is {card_on_table}\n")

            # Selecting a card from matched cards to play
            while matched_cards and count < 1 and (0 <= card_position <= len(matched_cards)):
                count+=1
                position = input(f"Which card do you want to play? Select card position:")
                card_position = int(position)
                while card_position > (len(matched_cards)):
                    position = input(f"Please select a card position less than or equal to {len(matched_cards)}:")
                    card_position = int(position)
                print(f"\nTo match the card: {card_on_table}, the card selected is {matched_cards[card_position-1]}")
                if matched_cards[card_position-1][c] == card_on_table[c]:
                    print(f"\nThey have the same color: {card_on_table[c]}")
                elif matched_cards[card_position-1][n] == card_on_table[n]:
                    print(f"\nThey have the same number: {card_on_table[n]}")
                if matched_cards[card_position-1] in personal_hand:
                    personal_hand.remove(matched_cards[card_position-1])
        
        # When user runs out of cards, game is finished
        if len(personal_hand) == 0:
            print("Game is done. You win!")

    def reverse(self, card_on_table):
        """A method that allows the player to reverse the order of who goes next. 

        Args:
            card_on_table (lst): A list of dictionaries containing the card deck for Uno. Each dictionary describes the type, color, number, and function of 
                each individual card.

        Returns:
            lst: An updated version of "players" list with the updated order of who goes next. This is applicable for a 2 player game of 1 player versus a computer bot. 
        """
        
        # An example of the player's hand for this function
        player_hand = [
        {"Type" : "Reverse",
        "Color" : "Red",
        "Number" : "None",
        "Function" : "Reverse"}
        ]
        
        # Setting up the color and function variables for matching with the cards on the table
        c = "Color"
        f = "Function"
        
        # This shows what card is on the table, so the player can determine which card to play. If a card matches with the card on the table, it will go into the matched_cards list
        card_on_table = table_cards.pop(0)
        matched_cards = []
        
        # This shows the playing order of who goes first to last
        players = ["Player1", "Player2", "Player3", "Player4"]
        
        # This looks into the specific card on the player's hand
        for card in player_hand:
        
        # This checks if the card from the player's hand matches with the card table based on the same color. The matched card will go into the matched_cards list
            if card[c] == card_on_table[c]:
                matched_cards.append(card)
                
        # This looks at the matched card just added, which will reverse the order if the function of that card matches with reverse cards
                for card in matched_cards:
                    if card[f] == "Reverse":
                        print(f"{players[0]} has reversed the game order!")
                        return players.reverse()
                    else:
                        print("This card doesn't reverse!")
        
        # This checks if the card from the player's hand matches with the card table based on the same function. The matched card will go into the matched_cards list
            elif card[f] == card_on_table[f]:
                matched_cards.append(card)
        
        # This looks at the matched card just added, which will reverse the order if the function of that card matches with reverse cards
                for card in matched_cards:
                    if card[f] == "Reverse":
                        print(f"{players[0]} has reversed the game order!")
                        return players.reverse()
                    else:
                        print("This card doesn't reverse!")
                        
        # If the card in the player's hand doesn't match with the card on the table
            else:
                return print("This card doesn't reverse!")
