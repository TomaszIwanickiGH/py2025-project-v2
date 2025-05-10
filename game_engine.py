from typing import List
from classes import Player, Deck, Card
from hand_evaluator import hand_rank
import random

class InvalidActionError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class GameEngine:
    def __init__(self, players: List[Player], deck: Deck,
                 small_blind: int = 25, big_blind: int = 50):
        self.players = players
        self.deck = deck
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0

    def play_round(self) -> None:
        self.pot = 0
        self.deck.shuffle()

        # 1. Blindy
        print("Pobieranie blindów...")
        self.players[0]._Player__stack_ -= self.small_blind
        self.players[1]._Player__stack_ -= self.big_blind
        self.pot += self.small_blind + self.big_blind

        # 2. Rozdanie kart
        self.deck.deal(self.players)
        for player in self.players:
            if player.get_name() == "Human":
                print("Twoje karty:", player.cards_to_str())

        # 3. Zakłady
        current_bet = self.big_blind
        for player in self.players:
            action = self.prompt_bet(player, current_bet)
            if action == 'fold':
                winner = self.players[1] if player == self.players[0] else self.players[0]
                winner._Player__stack_ += self.pot
                print(f"{player.get_name()} spasował. {winner.get_name()} wygrywa {self.pot} żetonów.")
                return

            elif action == 'raise':
                raise_amount = 50  # stała wartość podbicia (dla uproszczenia)
                current_bet += raise_amount
                player._Player__stack_ -= current_bet
                self.pot += current_bet

            elif action in ['call', 'check']:
                player._Player__stack_ -= current_bet
                self.pot += current_bet

        # 4. Wymiana kart
        for player in self.players:
            if player.get_name() == "Human":
                print("Twoje karty:", player.cards_to_str())
                try:
                    indices_str = input("Podaj indeksy kart do wymiany (np. 0 2 4): ")
                    indices = list(map(int, indices_str.strip().split()))
                    new_hand = self.exchange_cards(player.get_player_hand(), indices)
                    player._Player__hand_ = new_hand
                except (ValueError, IndexError):
                    print("Błędne indeksy – żadna karta nie została wymieniona.")
            else:
                # Bot wymienia losowo do 3 kart
                count = random.randint(0, 3)
                indices = random.sample(range(5), count)
                new_hand = self.exchange_cards(player.get_player_hand(), indices)
                player._Player__hand_ = new_hand

        # 5. Showdown
        winner = self.showdown()
        winner._Player__stack_ += self.pot
        print(f"Zwycięzca: {winner.get_name()}, otrzymuje {self.pot} żetonów.")

    def prompt_bet(self, player: Player, current_bet: int) -> str:
        """Pobiera akcję od gracza (human lub bot) — check/call/raise/fold."""
        while True:
            try:
                action = input(f"{player.get_name()} - aktualna stawka: {current_bet}. "
                               f"Dostępne akcje: check, call, raise, fold. Co robisz? ").lower()

                # Obsługa nieprawidłowych akcji
                if action not in ['check', 'call', 'raise', 'fold']:
                    raise InvalidActionError("Nieprawidłowa akcja. Wybierz 'check', 'call', 'raise' lub 'fold'.")

                # Sprawdzanie warunku dla 'raise'
                if action == 'raise':
                    raise_amount = int(input("Podaj wysokość podbicia: "))
                    if raise_amount > player.get_stack_amount():
                        raise InsufficientFundsError("Brak wystarczających środków na podbicie.")
                    return action, raise_amount

                return action, 0  # Dla 'check', 'call', 'fold'

            except ValueError:
                print("Błąd wejścia! Proszę podać liczbę (gdy jest wymagane).")
            except InvalidActionError as e:
                print(e)
            except InsufficientFundsError as e:
                print(e)

    def exchange_cards(self, hand: List[Card], indices: List[int]) -> List[Card]:
        """
        hand     – 5 kart gracza
        indices  – lista indeksów (0–4) do wymiany
        Zwraca: nową listę 5 kart.
        Stare karty odkłada na spód talii.
        """
        if not all(0 <= idx < 5 for idx in indices):
            raise IndexError("Indeks karty do wymiany musi być w zakresie 0-4.")

        new_cards = [self.deck.draw() for _ in indices]  # Zmieniamy deck na self.deck

        # Wymiana kart
        for i, idx in enumerate(indices):
            old_card = hand[idx]
            hand[idx] = new_cards[i]
            self.deck.discard_to_bottom(old_card)  # Zmieniamy deck na self.deck

        return hand

        return hand

    def showdown(self) -> Player:
        ranked_players = []
        for player in self.players:
            hand_values = [card.get_value() for card in player.get_player_hand()]
            strength = hand_rank(hand_values)
            ranked_players.append((strength, player))

        ranked_players.sort(reverse=True, key=lambda x: x[0])
        return ranked_players[0][1]
