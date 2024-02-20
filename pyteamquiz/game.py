from typing import Set, Dict, Tuple
import random
from .question import QuestionCatalogueFile, Question
from .errors import *

class Game():
    def __init__(self, catalgogues:Set[QuestionCatalogueFile], teams:Set[str], questions_per_team:int):
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

        # Ensure there are at least 2 teams
        if len(self.teams) < 2:
            raise NotEnoughTeamsError("At least two teams are required.")

        # Ensure team name is not too long
        for team in self.teams:
            if not 1 <= len(team) <= 30:
                raise TeamNameError("Team name must be between 1 and 30 chars.")

        # Ensure each team gets the desired number of questions
        questions_per_team = max(1, questions_per_team)
        if len(self.questions) < len(self.teams) * questions_per_team:
            raise NotEnoughQuestionsError("You have not enough questions in the selected catalogues. Select more catalogues.")
        self.questions = self.questions[:(len(self.teams) * questions_per_team)]

        # Init
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