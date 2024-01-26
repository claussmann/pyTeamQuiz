import random
from typing import List, Tuple
from .errors import *

class Question():
    def __init__(self, question_text, correct_answer, *fake_answers):
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.answers = set(fake_answers)
        self.answers.add(correct_answer)
        if not 1 < len(self.answers) <= 10:
            raise InvalidAnswerCount("You 2 to 10 different answers.")
        for answer in self.answers:
            if not 0 < len(answer) <= 150:
                raise AnswerSizeError("Answer length must be 1 to 150 chars.")
        if not 0 < len(self.question_text) <= 300:
            raise QuestionSizeError("Question length must be 1 to 300 chars.")

    def get_question_text(self) -> str:
        return self.question_text

    def get_answer_options(self) -> List[str]:
        ret = list(self.answers)
        random.shuffle(ret)
        return ret

    def check_answer(self, answer) -> bool:
        return answer == self.correct_answer

    def get_correct_answer(self) -> str:
        return self.correct_answer


class QuestionCatalogueFile():
    def __init__(self, filename):
        self.catalogue = list()
        in_file = open(filename, "r")
        for line in in_file:
            if line.startswith("#") or line == "" or line.isspace():
                continue
            self.catalogue.append(self.parse_line(line))
        in_file.close()

    @staticmethod
    def parse_line(line) -> Question:
        parts = line.split(";;")
        parts = [p for p in parts if p != ""]
        if len(parts) < 3:
            raise ValueError("File format is not correct.")
        return Question(parts[0], parts[1], *parts[2:])

    def get_question_list(self) -> List[Question]:
        return list(self.catalogue)