import html
import requests
import random

ENDPOINT = "https://opentdb.com/api.php"
NPPOINT_ENDPOINT_2 = "https://api.npoint.io/62224aa142fb44e52a94"
NPPOINT_ENDPOINT_4 = "https://api.npoint.io/1f98edab6fc5431d7356"

questions = []
options = []
correct_indices = []  # List to store the index of the correct option for each question
response = None


def get_quiz(amount, chapter):
    amount = int(amount)
    chapter = int(chapter)
    global response
    if chapter == 2:
        response = requests.get(NPPOINT_ENDPOINT_2)
    elif chapter == 4:
        response = requests.get(NPPOINT_ENDPOINT_4)
    data = response.json()['results']
    random.shuffle(data)
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
    return quiz_data[:amount]


