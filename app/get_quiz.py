import html
import requests
import random

ENDPOINT = "https://opentdb.com/api.php"

questions = []
options = []
correct_indices = []  # List to store the index of the correct option for each question


def get_quiz(amount, difficulty, type):
    parameters = {
        'amount': amount,
        'category': 17,
        'difficulty': difficulty,
        'type': type
    }
    response = requests.get(ENDPOINT, params=parameters)
    data = response.json()['results']
    quiz_data = []
    global questions, options, correct_indices
    questions.clear()
    options.clear()
    correct_indices.clear()  # Clear the correct_indices list for each new quiz
    for idx, el in enumerate(data):
        question = html.unescape(el['question'])
        correct_answer = html.unescape(el['correct_answer'])
        incorrect_answers = [html.unescape(answer) for answer in el['incorrect_answers']]
        options = random.sample(incorrect_answers + [correct_answer], len(incorrect_answers) + 1)
        is_correct = options.index(correct_answer)
        quiz_data.append({
            'idx': idx,
            'question': question,
            'options': options,
            'is_correct': is_correct,
            'len': len(questions)
        })
    return quiz_data
