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
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['c', 'd', 'h', 's']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        for player in players:
            for _ in range(5):
                card = self.cards.pop()
                player.take_card(card)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            raise ValueError("Talia jest pusta.")
        return self.cards.pop()

    def discard_to_bottom(self, card: Card):
        self.cards.insert(0, card)


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
