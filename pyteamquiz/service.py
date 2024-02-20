from . import games, catalogues
from .game import Game
import secrets
from typing import List, Set, Tuple, Dict

def get_available_catalogues() -> List[str]:
    ret = list(catalogues.keys())
    ret.sort()
    return ret

def new_game(catalogue_names: Set[str], team_names: Set[str], questions_per_team: int) -> str:
    token = secrets.token_hex(16)
    selected_catalogues = [catalogues[x] for x in catalogue_names]
    games[token] = Game(selected_catalogues, team_names, questions_per_team)
    return token

def whose_turn(game_id: str) -> str:
    return games[game_id].whose_turn()

def get_current_question_text(game_id: str) -> str:
    return games[game_id].get_question().get_question_text()

def get_current_question_options(game_id: str) -> List[str]:
    return games[game_id].get_question().get_answer_options()

def submit_answer(game_id: str, answer: str) -> bool:
    return games[game_id].submit_answer(answer)

def game_finished(game_id) -> bool:
    return not games[game_id].has_next()

def get_scores(game_id) -> Dict[str, int]:
    return games[game_id].get_scores()