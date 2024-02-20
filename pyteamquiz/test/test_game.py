import pytest
from pyteamquiz.question import *
from pyteamquiz.errors import *
from pyteamquiz.game import *
import os

def catalogue_1():
    content = """
What is correct 1?;;A;;B;;C;;D
What is correct 2?;;A;;B;;C;;D;;E
"""
    filename = "testfile-aesfhdshdfs2132312.txt"
    f = open(filename, "w")
    f.write(content)
    f.close()
    catalogue = QuestionCatalogueFile(filename)
    os.remove(filename)
    return catalogue

def catalogue_2():
    content = """
Foo?;;A;;B;;C;;D
Bar?;;A;;B;;C
"""
    filename = "testfile-aesfhdshdfs2132312.txt"
    f = open(filename, "w")
    f.write(content)
    f.close()
    catalogue = QuestionCatalogueFile(filename)
    os.remove(filename)
    return catalogue

def test_game_teams_turn():
    g = Game({catalogue_1(), catalogue_2()}, {"Team A", "Team B"}, 1)
    whose_turn = g.whose_turn()
    assert g.submit_answer("A") == (True, "A")
    assert whose_turn != g.whose_turn()

def test_game_error_when_questions_empty():
    g = Game({catalogue_1(), catalogue_2()}, {"Team A", "Team B"}, 2)
    assert g.submit_answer("A") == (True, "A")
    assert g.has_next()
    g.get_question()
    assert g.submit_answer("A") == (True, "A")
    assert g.has_next()
    assert g.submit_answer("A") == (True, "A")
    assert g.has_next()
    g.get_question()
    assert g.submit_answer("A") == (True, "A")
    assert not g.has_next()
    with pytest.raises(OutOfQuestionError):
        g.get_question()

def test_game_exception_when_too_few_questions():
    with pytest.raises(NotEnoughQuestionsError):
        # Every team must get at least one question
        g = Game({}, {"Team A", "Team B", "Team C"}, 0)
    with pytest.raises(NotEnoughQuestionsError):
        g = Game({catalogue_1()}, {"Team A", "Team B", "Team C"}, 1)

def test_game_every_player_same_number_questions():
    # 1 question for each of 3 teams
    g = Game({catalogue_1(), catalogue_2()}, {"Team A", "Team B", "Team C"}, 1)
    g.submit_answer("A")
    g.get_question()
    g.submit_answer("A")
    g.get_question()
    g.submit_answer("A")
    assert not g.has_next()

def test_game_at_least_two_teams():
    with pytest.raises(NotEnoughTeamsError):
        g = Game({catalogue_1()}, {}, 1)
    with pytest.raises(NotEnoughTeamsError):
        g = Game({catalogue_1()}, {"Team A"}, 1)
