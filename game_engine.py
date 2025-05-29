from typing import List
from classes import Player, Deck, Card
from hand_evaluator import hand_rank
import random
from src.fileops.session_manager import SessionManager
from datetime import datetime
import uuid

class InvalidActionError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class GameEngine:
    def __init__(self, players: List[Player], deck: Deck,
                 small_blind: int = 25, big_blind: int = 50,
                 from_loaded_session: bool = False,
                 game_id: str = None):
        self.players = players
        self.deck = deck
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0
        self.bets_log = []
        self.from_loaded_session = from_loaded_session
        self.game_id = game_id or str(uuid.uuid4())  # użyj przekazanego lub generuj nowy

    def play_round(self) -> None:
        session_manager = SessionManager()
        self.pot = 0
        self.bets_log = []
        self.deck.shuffle()

        # 1. Blindy
        print("Pobieranie blindów...")
        self.players[0]._Player__stack_ -= self.small_blind
        self.players[1]._Player__stack_ -= self.big_blind
        self.pot += self.small_blind + self.big_blind

        self.bets_log.append({
            "stage": "preflop",
            "player_id": 1,
            "action": "small_blind",
            "amount": self.small_blind,
            "pot": self.pot
        })
        self.bets_log.append({
            "stage": "preflop",
            "player_id": 2,
            "action": "big_blind",
            "amount": self.big_blind,
            "pot": self.pot
        })

        # 2. Rozdanie kart
        if not self.from_loaded_session:
            self.deck.deal(self.players)
        for player in self.players:
            if player.get_name() == "Human":
                print("Twoje karty:", player.cards_to_str())

        # 3. Zakłady
        current_bet = self.big_blind
        for i, player in enumerate(self.players):
            action, amount = self.prompt_bet(player, current_bet)

            if action == 'fold':
                winner = self.players[1] if player == self.players[0] else self.players[0]
                winner._Player__stack_ += self.pot
                print(f"{player.get_name()} spasował. {winner.get_name()} wygrywa {self.pot} żetonów.")
                return

            elif action == 'raise':
                player._Player__stack_ -= current_bet + amount
                self.pot += current_bet + amount
                self.bets_log.append({
                    "stage": "betting",
                    "player_id": i + 1,
                    "action": "raise",
                    "amount": amount,
                    "pot": self.pot
                })

            elif action in ['call', 'check']:
                player._Player__stack_ -= current_bet
                self.pot += current_bet
                self.bets_log.append({
                    "stage": "betting",
                    "player_id": i + 1,
                    "action": action,
                    "amount": current_bet,
                    "pot": self.pot
                })

        # 4. Wymiana kart
        for player in self.players:
            if player.get_name() == "Human":
                print("Twoje karty:", player.cards_to_str())
                try:
                    indices_str = input("Podaj indeksy kart do wymiany (np. 0 2 4): ")
                    indices = list(map(int, indices_str.strip().split()))
                    new_hand = self.exchange_cards(player, player.get_player_hand(), indices)
                    player._Player__hand_ = new_hand
                except (ValueError, IndexError):
                    print("Błędne indeksy – żadna karta nie została wymieniona.")
            else:
                count = random.randint(0, 3)
                indices = random.sample(range(5), count)
                new_hand = self.exchange_cards(player, player.get_player_hand(), indices)
                player._Player__hand_ = new_hand

        # 5. Showdown
        print("\nKarty graczy przed rozstrzygnięciem:")
        for player in self.players:
            print(f"{player.get_name()}: {player.cards_to_str()}")

        winner = self.showdown()
        winner._Player__stack_ += self.pot
        print(f"Zwycięzca: {winner.get_name()}, otrzymuje {self.pot} żetonów.")

        # 6. Zapis sesji
        session_data = {
            "game_id": self.game_id,
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "showdown",
            "players": [
                {"id": 1, "name": self.players[0].get_name(), "stack": self.players[0].get_stack_amount()},
                {"id": 2, "name": self.players[1].get_name(), "stack": self.players[1].get_stack_amount()}
            ],
            "deck": [card.to_storage_str() for card in self.deck.cards],
            "hands": {
                "1": [card.to_storage_str() for card in self.players[0].get_player_hand()],
                "2": [card.to_storage_str() for card in self.players[1].get_player_hand()]
            },
            "bets": self.bets_log,
            "current_player": None,
            "pot": self.pot
        }

        session_manager.save_session(session_data)

    def prompt_bet(self, player: Player, current_bet: int) -> tuple[str, int]:
        """Pobiera akcję od gracza (human lub bot) — check/call/raise/fold."""
        while True:
            try:
                action = input(f"{player.get_name()} - aktualna stawka: {current_bet}. "
                               f"Dostępne akcje: check, call, raise, fold. Co robisz? ").lower()

                if action not in ['check', 'call', 'raise', 'fold']:
                    raise InvalidActionError("Nieprawidłowa akcja. Wybierz 'check', 'call', 'raise' lub 'fold'.")

                if action == 'raise':
                    raise_amount = int(input("Podaj wysokość podbicia: "))
                    if raise_amount > player.get_stack_amount():
                        raise InsufficientFundsError("Brak wystarczających środków na podbicie.")
                    return action, raise_amount

                return action, 0

            except ValueError:
                print("Błąd wejścia! Proszę podać liczbę.")
            except InvalidActionError as e:
                print(e)
            except InsufficientFundsError as e:
                print(e)

    def exchange_cards(self, player: Player, hand: List[Card], indices: List[int]) -> List[Card]:
        if not all(0 <= idx < 5 for idx in indices):
            raise IndexError("Indeks karty do wymiany musi być w zakresie 0-4.")

        new_cards = [self.deck.draw() for _ in indices]
        for i, idx in enumerate(indices):
            old_card = hand[idx]
            new_card = new_cards[i]
            hand[idx] = new_card
            self.deck.discard_to_bottom(old_card)
            print(f"{player.get_name()} wymienił kartę {old_card} → {new_card}")

        return hand

    def showdown(self) -> Player:
        ranked_players = []
        for player in self.players:
            hand_values = [card.get_value() for card in player.get_player_hand()]
            strength = hand_rank(hand_values)
            ranked_players.append((strength, player))

        ranked_players.sort(reverse=True, key=lambda x: x[0])
        return ranked_players[0][1]
