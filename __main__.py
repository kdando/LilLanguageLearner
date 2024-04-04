from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap

from spanish_vocab import spanish_words as words
import random

# Create app
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'a2b2c2d2e2f2g'

# Configure session cookie settings
app.config.update( 
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE='Lax',  # Restrict cookie to same-site requests
    SESSION_COOKIE_SECURE=True  # Only send cookie over HTTPS
)

##############

#####################FUNCTIONS

def greet_user(username):
    return f"Hello, {username}! Welcome to the Lil Language Learner.\nThis app will help you learn the 100 most common words of your chosen language - a solid basis to actually communicate!"

##########INCREMENT CURRENT QUESTION

def increment_current_question():
    if 'current_question' not in session:
        session['current_question'] = 1
    else:
        session['current_question'] += 1

#########SET QUESTION
#could be cleaner

def set_question():
    current_word = random.choice(words)
    spanish_word = list(current_word.keys())[0]
    english_translation = current_word[spanish_word]
    return spanish_word, english_translation

#########CHECK ANSWER

def check_answer(spanish_word, english_translation, answer):
    if answer.lower() in english_translation:
        session['score'] += 1
        return "Correct!"
    else:
        return f"Incorrect :( '{spanish_word}' means '{english_translation[0]}'."

####################ROUTES

#if method is post that means form has been submitted and quiz starts, if its get then user is visiting the welcome page for the first time and hasnt chosen quiz settings (i.e. total questions)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        session.clear()
        return render_template("index.html")
    
    if request.method == "POST":
        session['username'] = request.form.get("username")
        session['total_questions'] = request.form.get("total_questions")
        session['score'] = 0
        session['current_question'] = 1
        new_question = set_question()
        session['spanish_word'] = new_question[0]
        session['english_translation'] = new_question[1]
        return render_template("quiz.html", greeting=greet_user(session["username"]))
    

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    # increment the current question number
    session['current_question'] += 1

    # if posting, i.e. an answer given..
    if request.method == "POST":
        #check previous answer
        session['answer'] = request.form.get('answer')
        check_answer(session['spanish_word'], session['english_translation'], session['answer'])

        #having checked last given answer, we go to results if we've reached last question
        #this will only happen on POST route as GET would mean no answers yet given
        if session['current_question'] > int(session['total_questions']):
            return render_template("result.html")

        #set a new question
        new_question = set_question()
        session['spanish_word'] = new_question[0]
        session['english_translation'] = new_question[1]

        #render quiz again with new question
        return render_template("quiz.html", greeting=greet_user(session['username']))
    
    #if method is GET, i.e. quiz page loads for first time
    return render_template("quiz.html", greeting=greet_user(session['username']))

@app.route("/result", methods=["GET", "POST"])
def result():
    return render_template("result.html")

#####################

if __name__ == '__main__':
    app.run(debug=True)

