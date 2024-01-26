import pytest
from pyteamquiz.question import *
from pyteamquiz.errors import *
import os

def test_question_get_answer_options():
    q = Question("Who is a jedi?", "Yoda", "Palpatine", "Jabbah", "Boba")
    options = q.get_answer_options()
    assert len(options) == 4
    assert "Yoda" in options
    assert "Palpatine" in options
    assert "Jabbah" in options
    assert "Boba" in options


def test_question_check_answer():
    q = Question("Who is a jedi?", "Yoda", "Palpatine", "Jabbah", "Boba")
    options = q.get_answer_options()
    for answer in options:
        if answer == "Yoda":
            assert q.check_answer(answer)
        else:
            assert not q.check_answer(answer)
    assert q.get_question_text() == "Who is a jedi?"


def test_question_illegal_number_of_answers():
    with pytest.raises(InvalidAnswerCount):
        q = Question("What is a prime?", "7")
    with pytest.raises(InvalidAnswerCount):
        q = Question("What is the first letter?", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K")


def test_question_illegal_answer_length():
    with pytest.raises(AnswerSizeError):
        q = Question("Foo?", "7", "")
    with pytest.raises(AnswerSizeError):
        q = Question("Bar?", "A", "B"*170, "C")


def test_question_illegal_text_length():
    with pytest.raises(QuestionSizeError):
        q = Question("", "A", "B")
    with pytest.raises(QuestionSizeError):
        q = Question("?"*310, "A", "B", "C")


def test_question_get_text():
    q = Question("What is an odd number?", "1", "4")
    assert q.get_question_text() == "What is an odd number?"


def test_question_catalogue_file():
    content ="""
# This is a comment
What is correct 1?;;A;;B;;C;;D
What is correct 2?;;A;;B;;C
# This is a comment
What is correct 3?;;A;;B;;C;;D;;E
What is correct 4?;;A;;B;;C;;

"""
    filename = "testfile-aesfhdshdfs2132312.txt"
    f = open(filename, "w")
    f.write(content)
    f.close()
    catalogue = QuestionCatalogueFile(filename)
    os.remove(filename)
    assert len(catalogue.get_question_list()) == 4


def test_question_catalogue_parse_line():
    q = QuestionCatalogueFile.parse_line("What is a prime?;;7;;9;;12;;27")
    options = q.get_answer_options()
    assert len(options) == 4
    assert "7" in options
    assert "9" in options
    assert "12" in options
    assert "27" in options


def test_question_catalogue_parse_incorrect_line():
    with pytest.raises(ValueError):
        q = QuestionCatalogueFile.parse_line("What is correct?;A;B;C")
    with pytest.raises(ValueError):
        q = QuestionCatalogueFile.parse_line("What is correct?;;A")
    with pytest.raises(ValueError):
        q = QuestionCatalogueFile.parse_line("What is correct?;;A;;")


def test_question_catalogue_parse_line_with_empty_answers():
    q = QuestionCatalogueFile.parse_line("What is correct?;;A;;B;;C;;")
    options = q.get_answer_options()
    assert len(options) == 3
    assert "A" in options
    assert "B" in options
    assert "C" in options