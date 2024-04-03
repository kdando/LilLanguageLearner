from flask import Flask, render_template, request, session
from spanish_vocab import spanish_words as words
import random


app = Flask(__name__)
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

#########CHECK IF ALL QUESTIONS ANSWERED
def check_all_questions_answered():
    return session.get('current_question', 0) >= int(session.get('total_questions'), 0)

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
    if request.method == "POST":
        session['username'] = request.form.get("username")
        session['total_questions'] = request.form.get("total_questions")
        session['score'] = 0
        return render_template("quiz.html", greeting=greet_user(session["username"]))
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    #if all qs answered we go to results

    if check_all_questions_answered():
        print("all answered")
        return render_template("result.html")
    
    #if not all qs answered and we posted we check, then go to quiz again with a new q
    if request.method == "POST":
        increment_current_question()
        # if check_all_questions_answered():
        #     return render_template("result.html")
        # else:

        new_question = set_question()
        spanish_word = new_question[0]
        english_translation = new_question[1]

        return render_template("quiz.html", greeting=greet_user(session['username']), spanish_word=spanish_word, english_translation=english_translation)
    
    #if method is get, i.e. quiz page loads for first time
    return render_template("quiz.html", greeting=greet_user(session['username']), spanish_word=spanish_word, english_translation=english_translation)

@app.route("/result", methods=["GET", "POST"])
def result():
    return render_template("result.html")

#####################

if __name__ == '__main__':
    app.run(debug=True)

