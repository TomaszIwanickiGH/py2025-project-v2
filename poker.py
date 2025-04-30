import random

def histogram(lst):
    hist = {}
    for item in lst:
        hist[item] = hist.get(item, 0) + 1
    return hist

def is_rank_sequence(hand):
    rank_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ranks = [card[0] for card in hand]

    if 'A' and '2' and '3' and '4' and '5' in ranks:
        ranks = ['1' if rank == 'A' else rank for rank in ranks]

    rank_indices = [rank_order.index(rank) for rank in ranks]
    rank_indices.sort()

    return rank_indices == list(range(rank_indices[0], rank_indices[0] + 5))

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


def hand_rank(hand):
    hand_rank_list = [card[0] for card in hand]
    hand_color_list = [card[1] for card in hand]

    hand_rank_histogram = histogram(hand_rank_list)
    hand_color_histogram = histogram(hand_color_list)

    is_hand_rank_sequence = is_rank_sequence(hand)

    hand_strength = 0

    # Sprawdzamy poker królewski: 5 kart w tym samym kolorze, po kolei, najwyższa to as
    if (5 in hand_color_histogram.values()) and ('A' in hand_rank_list) and is_hand_rank_sequence:
        hand_strength = 10
    # Sprawdzamy poker: 5 kart w tym samym kolorze, po kolei
    elif (5 in hand_color_histogram.values()) and is_hand_rank_sequence:
        hand_strength = 9
    # Sprawdzamy karete: 4 karty tej samej rangi
    elif 4 in hand_rank_histogram.values():
        hand_strength = 8
    # Sprawdzamy full house: 3 karty tej samej rangi i 2 karty tej samej rangi
    elif sorted(hand_rank_histogram.values()) == [2, 3]:
        hand_strength = 7
    # Sprawdzamy kolor: 5 kart w tym samym kolorze
    elif 5 in hand_color_histogram.values():
        hand_strength = 6
    # Sprawdzamy strit: 5 kart po kolei
    elif is_hand_rank_sequence:
        hand_strength = 5
    # Sprawdzamy trojkę: 3 karty tej samej rangi
    elif 3 in hand_rank_histogram.values():
        hand_strength = 4
    # Sprawdzamy dwie pary: 2 pary
    elif list(hand_rank_histogram.values()).count(2) == 2:
        hand_strength = 3
    # Sprawdzamy jedną parę: 1 para
    elif 2 in hand_rank_histogram.values():
        hand_strength = 2
    # Wysoka karta: brak par, trojek, czwórek itd.
    else:
        hand_strength = 1

    return hand_strength


player1 = Player(1000, "Player1")
player2 = Player(1000, "Player2")

deck = Deck()
deck.shuffle()

deck.deal([player1, player2])

print(f'{player1.get_name()} - {player1.cards_to_str()}')
print(f'{player2.get_name()} - {player2.cards_to_str()}')