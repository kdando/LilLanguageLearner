from flask import Flask, render_template, request
from spanish_vocab import spanish_words as words
import random

app = Flask(__name__)

#####################FUNCTIONS

def greet_user(username):
    return f"Hello, {username}! Welcome to the Lil Language Learner.\nThis app will help you learn the 100 most common words of your chosen language - a solid basis to actually communicate!"

def set_question():
    current_word = random.choice(words)
    spanish_word = list(current_word.keys())[0]
    english_translation = current_word[spanish_word]
    return spanish_word, english_translation

def run_quiz(spanish_word, english_translation, answer):
    if answer in english_translation:
        return "Correct!"
    else:
        return f"Incorrect :( '{spanish_word}' means '{english_translation[0]}'."

####################ROUTES

@app.route("/", methods=["GET", "POST"])
def index():
    username = None
    if request.method == "POST":
        username = request.form.get("username")
        return render_template("quiz.html")
    return render_template("index.html",username=username)

@app.route("/quiz", methods=["POST"])
def quiz():
    spanish_word, english_translation = set_question()
    return render_template('quiz.html', greeting=greet_user(request.form.get("username")), spanish_word=spanish_word, english_translation=english_translation)

@app.route("/result", methods=["POST"])
def result():
    answer = request.form.get("answer")
    spanish_word = request.form.get("spanish_word")
    english_translation = request.form.get("english_translation")
    judgement = run_quiz(spanish_word, english_translation, answer)
    return render_template("result.html", result=judgement, spanish_word=spanish_word, english_translation=english_translation)

#####################

if __name__ == '__main__':
    app.run(debug=True)

