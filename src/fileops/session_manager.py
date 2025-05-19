import os
import json
from datetime import datetime
from typing import Dict


class SessionManager:
    def __init__(self, data_dir: str = 'data'):
        """Inicjalizuje katalog, w którym przechowywane będą pliki sesji."""
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_session(self, session: Dict) -> None:
        """Zapisuje stan gry i historię zakończonych rozdań do pliku."""
        try:
            game_id = session.get("game_id")
            if not game_id:
                raise ValueError("Brakuje game_id w sesji")

            filename = os.path.join(self.data_dir, f"session_{game_id}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(session, f, indent=4, ensure_ascii=False)
        except (IOError, ValueError) as e:
            print(f"Błąd zapisu sesji: {e}")

    def load_session(self, game_id: str) -> Dict:
        """Ładuje sesję gry z pliku i zwraca strukturę pozwalającą na kontynuację rozgrywki."""
        try:
            filename = os.path.join(self.data_dir, f"session_{game_id}.json")
            with open(filename, "r", encoding="utf-8") as f:
                session = json.load(f)
            return session
        except FileNotFoundError:
            print(f"Nie znaleziono pliku dla game_id: {game_id}")
            return {}
        except json.JSONDecodeError:
            print(f"Nieprawidłowy format JSON w pliku sesji.")
            return {}
