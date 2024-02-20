import os
from .question import QuestionCatalogueFile



# Settings (possibly from env variables)
settings = {
    "QUESTION_CATALOGUE_DIR": os.environ.get("QUESTION_CATALOGUE_DIR", "../questions/"),
}



# Read Question Catalogues
def _is_valid_filename(fn):
    if not fn.endswith(".txt"):
        return False
    fn = fn[:len(fn) - 4]
    return len(fn) > 0 and not fn.isspace()

games = dict()
question_catalogue_dir = settings["QUESTION_CATALOGUE_DIR"]
if os.path.isdir(question_catalogue_dir):
    catalogues = {
        fn[:len(fn) - 4]: QuestionCatalogueFile(filename=os.path.join(question_catalogue_dir, fn))
        for fn in os.listdir(question_catalogue_dir)
        if _is_valid_filename(fn)
    }
else:
    catalogues = dict()