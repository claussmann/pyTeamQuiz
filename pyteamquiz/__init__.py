import os
from .question import QuestionCatalogueFile

settings = {
    "QUESTION_CATALOGUE_DIR": os.environ.get("QUESTION_CATALOGUE_DIR", "../questions/"),
}

games = dict()
question_catalogue_dir = settings["QUESTION_CATALOGUE_DIR"]
if os.path.isdir(question_catalogue_dir):
    catalogues = {
        filename: QuestionCatalogueFile(filename=os.path.join(question_catalogue_dir, filename))
        for filename in os.listdir(question_catalogue_dir)
        if filename.endswith(".txt")
    }
else:
    catalogues = dict()