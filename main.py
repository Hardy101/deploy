from flask import Flask, render_template, url_for, request
from get_quiz import get_quiz

app = Flask(__name__)


# Custom Filters
def custom_enumerate(iterable, start=0):
    return enumerate(iterable, start=start)


app.jinja_env.filters['enumerate'] = custom_enumerate


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/create-quiz')
def create_quiz():
    return render_template('pages/create-quiz.html')


@app.route('/coming-soon')
def coming_soon():
    return render_template('pages/coming_soon.html')


@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')


@app.route('/endquiz')
def endquiz():
    return render_template('pages/endquiz.html')


@app.route('/select-quiz')
def select_quiz():
    return render_template('pages/select_quiz.html')


@app.route('/take-quiz', methods=['GET', 'POST'])
def take_quiz():
    amount = request.form['amount']
    difficulty = request.form['difficulty']
    quiz_type = request.form['type']
    quiz_data = get_quiz(amount, difficulty, quiz_type)
    return render_template('pages/spark.html', quiz_data=quiz_data, quiz_contents=amount)


@app.route('/quiz')
def quiz():
    return render_template('pages/quiz.html')


@app.route('/login')
def login():
    return render_template('pages/login.html')


@app.route('/recover')
def recover():
    return render_template('pages/recover.html')


@app.route('/register')
def register():
    return render_template('pages/register.html')


@app.route("/<page>")
def notfound(page):
    return render_template('pages/notFound.html')


    # if __name__ == "__main__":
    #     app.run(debug=True)
