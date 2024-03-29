from flask import Flask, redirect, render_template, request
from . import service
from .errors import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def start():
    return render_template('start.html', catalogue_names=service.get_available_catalogues())


@app.route("/", methods=["POST"])
def new_game():
    selected = set(filter(len, request.form.getlist('catalogues[]')))
    teams = set(filter(len, request.form.getlist('teams[]')))
    questions_per_team = int(request.form.get('q_per_team'))
    try:
        game_id = service.new_game(selected, teams, questions_per_team)
    except (NotEnoughQuestionsError, NotEnoughTeamsError, TeamNameError) as e:
        return render_template('error.html', msg=str(e))
    return render_template('created.html', game_id=game_id)

@app.route("/<game_id>/question", methods=["GET"])
def get_question(game_id:str):
    if service.game_finished(game_id):
        return render_template("finish.html", result=service.get_scores(game_id))
    return render_template('question.html',
        game_id=game_id,
        question_text=service.get_current_question_text(game_id),
        options=service.get_current_question_options(game_id),
        whose_turn=service.whose_turn(game_id),
        current_scores=service.get_scores(game_id)
        )

@app.route("/<game_id>/answer", methods=["POST"])
def answer_question(game_id:str):
    answer = request.form.get("anwer")
    correct, correct_answer = service.submit_answer(game_id, answer)
    return render_template('answer.html',
        game_id=game_id,
        correct=correct,
        correct_answer=correct_answer,
        current_scores=service.get_scores(game_id)
    )

