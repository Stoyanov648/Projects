from random import shuffle

SUITE = 'H D S C'.split()
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()


class Deck:
    """
    This is the deck class. This object will create a deck of cards to initiate play.
    You can then use this Deck List of cards to split in half and give to
    the players. It will use SUITE to create the deck. It should also have a
    method for splitting/cutting the deck in half and Shuffling the deck.
    """
    def __init__(self,):
        print("Creating new ordered deck")
        self.all_cards = [(s, r) for s in SUITE for r in RANKS]

    def shuffle(self):
        print("Shuffling the Deck!")
        shuffle(self.all_cards)

    def split_in_half(self):
        return (self.all_cards[:26], self.all_cards[26:])


class Hand:
    """
    This is the Hand class. Each player has a Hand, and can add or remove cards
    from the hand. There should be an add and remove card method here
    """
    def __init__(self,cards):
        self.cards = cards

    def __str__(self):
        return f"Contains {len(self.cards)} cards"

    def add(self, added_cards):
        self.cards.extend(added_cards)

    def remove_cards(self):
        return self.cards.pop(0)


class Player:
    """
    This is the PLayer class, which takes in a name and an instance of a Hand class object.
    The player can then play cards and check if they still have cards.
    """
    def __init__(self,name, hand):
        self.name = name
        self.hand = hand

    def play_card(self):
        drawn_card = self.hand.remove_cards()
        print(f"{self.name} has placed: {drawn_card}")
        print(f"\n")
        return drawn_card

    def remove_war_cards(self):
        war_cards = []
        # when the cards left in hand are 3 or less the index ot table_card[5][1] is crashing the program
        # that's why in such case the function returns tuple of 404s
        # once it returns them the program does a quick chech and if 404s are found on the table
        # The one who drops them will be disqualified due to no more cards to continue.
        if len(self.hand.cards) < 3:
            global disqualified
            disqualified = self.name

            return (404,404,404,404,404,404)
        else:
            for x in range(3):
                war_cards.append(self.hand.remove_cards())
            return war_cards

    def still_has_cards(self):
        """
        returns true if player still have cards
        """
        return len(self.hand.cards) != 0


def end_stats():
    """
    This function will be used only in case of gameover to print
    the result statisctics.
    """
    print(f"Game over, number of rounds: {str(total_rounds)}")
    print(f"a War happened {str(war_count)} times")
    print(f"a War DRAW happened {str(war_draw)} times")
    if len(pc.hand.cards) > len(player.hand.cards):

        print(f"{pc.name} Wins")
    else:

        print(f"{player.name} WINS")


# GAMEPLAY
# Creating a deck, shuffle and split
deck = Deck()
deck.shuffle()
half1, half2 = deck.split_in_half()

# Creating both players!
pc = Player('Computer', Hand(half1))  # Create a Hand object using half1
player = Player(input("Input your name here: "), Hand(half2))  # Create a Hand object using half2

stop = False
disqualified = ''
next_start = ''
total_rounds = 0
war_count = 0
war_draw = 0
# Starting a while loop which will end only in 2 scenarios
# 1 when one of the players lose all his cards
# 2 in case of a war if a player doesn't have enough cards to continue the battle
while player.still_has_cards() and pc.still_has_cards():

    total_rounds += 1
    print("Time for new round!")
    print("Here are the current standings")
    print(f"{player.name} has the count: {str(len(player.hand.cards))}")
    print(f"{pc.name} has the count: {str(len(pc.hand.cards))}")
    print("Play a card!")
    print('\n')

    table_cards = []
    # by default the Computer starts the game
    # in the end of every round the Winner becomes the one who starts the next round.
    # The code bellow is only conditions set by me or by the game rules.
    if next_start == 'human':
        human = True
        computer = False
        player_card = player.play_card()
        pc_card = pc.play_card()
        table_cards.append(player_card)
        table_cards.append(pc_card)
    else:
        human = False
        computer = True
        pc_card = pc.play_card()
        player_card = player.play_card()

        table_cards.append(pc_card)
        table_cards.append(player_card)
    if pc_card[1] == player_card[1]: # line 144 - 177 is only in case of WAR condition
        war_count += 1
        print("War!")

        table_cards.extend(player.remove_war_cards())
        table_cards.extend(pc.remove_war_cards())
        if 404 in table_cards:
            print(f"{disqualified} LOST! Not enough cards to continue the BATTLE!")
            end_stats()
            exit()
        elif table_cards[2][1] == table_cards[5][1]:
            print("War DRAW")
            print("In case of WAR DRAW both sides looses table cards")
            war_draw += 1
            continue
        if computer: # is the one who starts THEN:
            if RANKS.index(table_cards[2][1]) < RANKS.index(table_cards[5][1]):
                player.hand.add(table_cards)
                print(f"{player.name} WINS the round")
                next_start = 'human'
            elif RANKS.index(table_cards[2][1]) > RANKS.index(table_cards[5][1]):
                pc.hand.add(table_cards)
                print(f"{pc.name} WINS the round")
                next_start = 'pc'
        elif human: # but if the Human was the one who started THEN:
            if RANKS.index(table_cards[2][1]) > RANKS.index(table_cards[5][1]):
                player.hand.add(table_cards)
                print(f"{player.name} WINS the round")
                next_start = 'human'
            elif RANKS.index(table_cards[2][1]) < RANKS.index(table_cards[5][1]):
                pc.hand.add(table_cards)
                print(f"{pc.name} WINS the round")
                next_start = 'pc'
    else:
        if computer: # is the one who starts THEN:
            if RANKS.index(table_cards[0][1]) < RANKS.index(table_cards[1][1]):
                player.hand.add(table_cards)
                print(f"{player.name} WINS the round")
                next_start = 'human'
            elif RANKS.index(table_cards[0][1]) > RANKS.index(table_cards[1][1]):
                pc.hand.add(table_cards)
                print(f"{pc.name} WINS the round")
                next_start = 'pc'
        elif human: # but if the Human was the one who started THEN:
            if RANKS.index(table_cards[0][1]) > RANKS.index(table_cards[1][1]):
                player.hand.add(table_cards)
                print(f"{player.name} WINS the round")
                next_start = 'human'
            elif RANKS.index(table_cards[0][1]) < RANKS.index(table_cards[1][1]):
                pc.hand.add(table_cards)
                print(f"{pc.name} WINS the round")
                next_start = 'pc'

end_stats()

