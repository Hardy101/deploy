from flask import Flask, render_template, url_for, request, redirect
from get_quiz_t import get_quiz
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    question = db.Column(db.String(50), nullable=False)
    correct_answer = db.Column(db.String(250), nullable=False)
    incorrect_answer = db.Column(db.String(250), nullable=False)


# API Call
@app.route('/api.mindspark/<int:amount>')
def api():
    pass


@app.route('/addquestion', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        question_to_add = request.form['question']
        correct_answer = request.form['c_answer']
        incorrect_answer = request.form['ic_answer']
        new_question = Questions(question=question_to_add, correct_answer=correct_answer,
                                 incorrect_answer=incorrect_answer)
        db.session.add(new_question)
        db.session.commit()
    return render_template('test.html')


@app.route('/')
def index():
    return redirect(url_for('select_quiz'))
    # return render_template('index.html')


@app.route('/about')
def about():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/about.html')


@app.route('/create-quiz')
def create_quiz():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/create-quiz.html')


@app.route('/coming-soon')
def coming_soon():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/coming_soon.html')


@app.route('/dashboard')
def dashboard():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/dashboard.html')


@app.route('/endquiz')
def endquiz():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/endquiz.html')


@app.route('/select-quiz')
def select_quiz():
    return render_template('pages/select_quiz.html')


@app.route('/take-quiz', methods=['GET', 'POST'])
def take_quiz():
    amount = request.form['amount']
    if not amount or int(amount) < 1:
        return redirect(url_for('notfound', page='notfound'))
    else:
        # difficulty = request.form['difficulty']
        # quiz_type = request.form['type']
        quiz_data = get_quiz(amount)
        return render_template('pages/spark.html', quiz_data=quiz_data, quiz_contents=amount)


@app.route('/quiz')
def quiz():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/quiz.html')


@app.route('/login')
def login():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/login.html')


@app.route('/recover')
def recover():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/recover.html')


@app.route('/register')
def register():
    return redirect(url_for('select_quiz'))
    # return render_template('pages/register.html')


@app.route("/<page>")
def notfound(page):
    return render_template('pages/notFound.html')

<<<<<<< HEAD:app/main.py

if __name__ == "__main__":
    app.run(debug=True)
=======
>>>>>>> c84196ce5cff2c16a78f0075a4362e2bdff31637:main.py
