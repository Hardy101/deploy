import PyPDF2
import werkzeug.security
import requests
import random
from datetime import datetime

# OWN_ENDPOINT = 'http://127.0.0.1:5000/api'
ENDPOINT = 'https://api.npoint.io/099e5ac3feaf37dd4c81'
ENDPOINT_2 = 'https://api.npoint.io/0b3f47e967ceeab2d854'
google_books_endpoint = 'https://www.googleapis.com/books/v1/volumes'
API_KEY = 'AIzaSyChVvbQvSXosrxSsR8BoqtRPUzldldkyH0'


def get_today_date():
    today_datetime = datetime.now()
    today_date = today_datetime.strftime("%d/%m/%Y")
    return today_date


def get_book_info(query):
    params = {
        'q': query,
        'key': API_KEY
    }
    request = requests.get(google_books_endpoint, params=params)
    response = request.json()
    data = response['items']
    books = []
    for book in data:
        try:
            image_links = book['volumeInfo']['imageLinks']['smallthumbnail']
        except KeyError:
            image_links = 'static/img/cover-1.jpg'

        book_info = {
            'authors': book['volumeInfo']['authors'],
            'title': book['volumeInfo']['title'],
            'img': image_links  # Include the thumbnail URL in the book_info dictionary
        }
        books.append(book_info)
    return books


def get_quiz(amount):
    amount = int(amount)
    response = requests.get(ENDPOINT_2)
    data = response.json()
    questions = data[0]['questions'].split('/n')
    options = data[0]['options'].split('/n')
    options_list = [(option.replace('\n', '').split(',')) for option in options]
    quiz_data = []
    for idx, el in enumerate(questions):
        correct_answer = options_list[idx][0]
        random.shuffle(options_list[idx])
        question = el.replace('\n', '')
        is_correct = options_list[idx].index(correct_answer)
        quiz_data.append({
            'idx': idx,
            'question': question,
            'options': options_list[idx],
            'is_correct': is_correct,
            'len': len(questions)
        })
    random.shuffle(quiz_data)
    return quiz_data[:amount]


def hash_password(password):
    hashed_password = werkzeug.security.generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    return hashed_password


def extract_text(pdf):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    pdf.close()
    return text


def user_exists(email, db, users):
    existing_user = db.session.query(users).filter_by(email=email).first()
    if existing_user:
        return True
    else:
        return False
