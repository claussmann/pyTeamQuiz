from typing import Set, Dict, Tuple
import random
from .question import QuestionCatalogueFile, Question
from .errors import *

class Game():
    def __init__(self, catalgogues:Set[QuestionCatalogueFile], teams:Set[str]):
        self.questions = list()
        for catalogue in catalgogues:
            for q in catalogue.get_question_list():
                self.questions.append(q)
        random.shuffle(self.questions)
        self.teams = list(teams)
        self.scores = {
            team: 0
            for team in self.teams
        }
        self.round = 0
        self.current_question = None
        self._next_question()

    def get_question(self) -> Question:
        if self.current_question == None:
            raise OutOfQuestionError()
        return self.current_question

    def skip(self):
        self._next_question()

    def has_next(self) -> bool:
        return self.current_question != None

    def get_scores(self) -> Dict[str, int]:
        return dict(self.scores)

    def submit_answer(self, answer) -> Tuple[bool, str]:
        q = self.current_question
        self._next_question()
        if q.check_answer(answer):
            self.scores[self.whose_turn()] += 1
            self.round += 1
            return (True, q.get_correct_answer())
        self.round += 1
        return (False, q.get_correct_answer())

    def whose_turn(self) -> str:
        return self.teams[self.round % len(self.teams)]

    def _next_question(self):
        if self.questions == list():
            self.current_question = None
        else:
            self.current_question = self.questions.pop(0)