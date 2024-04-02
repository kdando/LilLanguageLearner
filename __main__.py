from flask import Flask, render_template
from spanish_vocab import spanish_words as words
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#####################

# def greet_user(name):
#     print(f"Hello, {name}! Welcome to the Lil Language Learner.\nThis app will help you learn the 100 most common words of your chosen language - a solid basis to actually communicate. You will be asked 10 questions at a time.\nPress Enter to start the quiz.")

# name = input("What's your name?\n")

# greet_user(name)

# score = 0
# language = words

# def run_quiz(score, language):

#     while score >= 0 and score < 5:
#         current_word = random.choice(words)
#         spanish_word = list(current_word.keys())[0]
#         english_translation = current_word[spanish_word]

#         users_answer = input(f"What does {spanish_word} mean?\n")

#         if users_answer in english_translation:
#             score += 1
#             print(f"Correct! Your current score is {score}.")
#         else:
#             score -= 1
#             print(f"Incorrect. '{spanish_word}' means '{english_translation[0]}'.\nYour current score is {score}.")


# run_quiz(score, language)

#####

if __name__ == '__main__':
    app.run(debug=True)

