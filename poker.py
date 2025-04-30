import random

class Card:
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        return (self.rank, self.suit)

    def __str__(self):
        return f'{self.rank}{Card.unicode_dict[self.suit]}'

class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']
        suits = ['c', 'd', 'h', 's']

        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        for player in players:
            for _ in range(5):
                card = self.cards.pop()
                player.take_card(card)

class Player:
    def __init__(self, money, name=""):
        self.__stack_ = money
        self.__name_ = name
        self.__hand_ = []

    def take_card(self, card):
        self.__hand_.append(card)

    def get_stack_amount(self):
        return self.__stack_

    def change_card(self, card, idx):
        old_card = self.__hand_[idx]
        self.__hand_[idx] = card
        return old_card

    def get_player_hand(self):
        return self.__hand_

    def cards_to_str(self):
        return ', '.join(str(card) for card in self.__hand_)

    def get_name(self):
        return self.__name_

player1 = Player(1000, "Player1")
player2 = Player(1000, "Player2")

deck = Deck()
deck.shuffle()

deck.deal([player1, player2])

print(f'{player1.get_name()} - {player1.cards_to_str()}')
print(f'{player2.get_name()} - {player2.cards_to_str()}')
