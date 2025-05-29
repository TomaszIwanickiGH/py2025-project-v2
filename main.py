from classes import Player, Deck, Card
from game_engine import GameEngine
from src.fileops.session_manager import SessionManager
import uuid

def reconstruct_players(saved_players, saved_hands):
    players = []
    for p in saved_players:
        player = Player(p["stack"], p["name"])
        hand_cards = [Card.from_str(card_str) for card_str in saved_hands[str(p["id"])]]
        player._Player__hand_ = hand_cards
        players.append(player)
    return players

def reconstruct_deck(deck_list):
    deck = Deck()
    deck.cards = [Card.from_str(card_str) for card_str in deck_list]
    return deck

def main():
    while True:
        choice = input("Wybierz: (N)owa gra czy (W)czytaj grę? ").strip().lower()
        if choice in ['n', 'w']:
            break
        print("Nieprawidłowy wybór. Wpisz 'N' lub 'W'.")

    if choice == 'w':
        session_id = input("Podaj game_id do wczytania: ").strip()
        session_manager = SessionManager()
        session = session_manager.load_session(session_id)

        if not session:
            print("Nie udało się wczytać gry.")
            return

        players = reconstruct_players(session["players"], session["hands"])
        deck = reconstruct_deck(session["deck"])

        engine = GameEngine(players, deck, from_loaded_session=True, game_id=session_id)
        engine.bets_log = session.get("bets", [])
        engine.pot = session.get("pot", 0)

        print(f"Wczytano grę {session_id}.")
        for player in players:
            print(f"{player.get_name()} ma {player.get_stack_amount()} żetonów.")
        engine.play_round()


    else:
        # Nowa gra
        deck = Deck()
        player_human = Player(1000, "Human")
        player_bot = Player(1000, "Bot")

        players = [player_human, player_bot]
        engine = GameEngine(players, deck)

        engine.play_round()

    for player in engine.players:
        print(f"{player.get_name()} ma teraz {player.get_stack_amount()} żetonów.")


if __name__ == "__main__":
    main()
