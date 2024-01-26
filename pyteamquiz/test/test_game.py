import pytest
from pyteamquiz.question import *
from pyteamquiz.errors import *
from pyteamquiz.game import *
import os

def get_catalogue_1():
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

def get_catalogue_2():
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
    g = Game(
        {get_catalogue_1(), get_catalogue_2()},
        {"Team A", "Team B"}
        )
    whose_turn = g.whose_turn()
    assert g.submit_answer("A") == (True, "A")
    assert whose_turn != g.whose_turn()

def test_game_error_when_questions_empty():
    g = Game(
        {get_catalogue_1(), get_catalogue_2()},
        {"Team A", "Team B"}
        )
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

