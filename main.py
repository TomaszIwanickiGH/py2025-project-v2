from classes import Player, Deck
from game_engine import GameEngine

def main():
    deck = Deck()
    player_human = Player(1000, "Human")
    player_bot = Player(1000, "Bot")

    players = [player_human, player_bot]

    engine = GameEngine(players, deck)

    engine.play_round()

    for player in players:
        print(f"{player.get_name()} ma teraz {player.get_stack_amount()} żetonów.")

if __name__ == "__main__":
    main()
