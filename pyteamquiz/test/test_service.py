import pytest
from pyteamquiz.question import *
from pyteamquiz.errors import *
from pyteamquiz.game import *
from pyteamquiz import service
from pyteamquiz import catalogues
import os


def catalogue_1():
    content = """
What is correct?;;A;;B;;C;;D
What is correct?;;A;;B;;C;;D;;E
What is correct?;;A;;B;;C;;D;;E
"""
    filename = "testfile-aesfhdshdfs2132312.txt"
    f = open(filename, "w")
    f.write(content)
    f.close()
    catalogue = QuestionCatalogueFile(filename)
    os.remove(filename)
    return catalogue

def test_game_creation():
    catalogues["Example"] = catalogue_1()
    token = service.new_game({"Example"}, {"Team A", "Team B"}, 1)
    assert service.get_current_question_text(token) == "What is correct?"
