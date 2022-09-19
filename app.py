from crypt import methods
from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "qwerty123"

boggle_game = Boggle()

N = 6

@app.route('/', methods=['POST'])
def home():
    """Show board and record"""
    N = request.form.get("N", 5)
    board = boggle_game.make_board(int(N))
    session["board"] = board
    session["N"] = N
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("home.html",
                            board=board,
                            highscore=highscore,
                            nplays = nplays)

@app.route('/check-word')
def check_word():
    """Check if word in dictionary"""
    board = session["board"]
    word = request.args["word"]
    N = session["N"]
    result = boggle_game.check_valid_word(board, word, N)

    return jsonify({"result": result})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session["nplays"] = nplays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)

@app.route('/about')
def about():
    """About Boggle"""
    return render_template("about.html")