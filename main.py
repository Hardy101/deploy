from flask import Flask, render_template, url_for, request, redirect
from get_quiz_t import get_quiz
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    accttype = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Questions(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    questiontype = db.Column(db.String(50), nullable=False)
    questions = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(200), nullable=False)
    privacy = db.Column(db.String(50), nullable=False)


# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    # return redirect(url_for('select_quiz'))
    return render_template('index.html')


@app.route('/create-quiz')
def create_quiz():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/create-quiz.html')


@app.route('/coming-soon')
def coming_soon():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/coming_soon.html')


@app.route('/dashboard/<username>')
def dashboard(username):
    user = Users.query.filter_by(username=username).first_or_404(description="No user with the provided username")
    # return redirect(url_for('select_quiz'))
    return render_template('pages/dashboard.html', user=user)


@app.route('/endquiz')
def endquiz():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/endquiz.html')


@app.route('/select-quiz')
def select_quiz():
    return render_template('pages/select_quiz.html')


@app.route('/quiz-info')
def quiz_info():
    return render_template('pages/quiz_info.html')


@app.route('/take-quiz', methods=['GET', 'POST'])
def take_quiz():
    amount = request.form['amount']
    if not amount or int(amount) < 1:
        return redirect(url_for('notfound', page='notfound'))
    else:
        chapter = request.form['chapter']
        # quiz_type = request.form['type']
        quiz_data = get_quiz(amount, chapter)
        return render_template('pages/take-quiz.html', quiz_data=quiz_data, quiz_contents=amount)


@app.route('/quiz')
def quiz():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/quiz.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/login.html')


@app.route('/recover')
def recover():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/recover.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@')[0]
        name = request.form['name']
        dob = request.form['dob']
        dob = request.form['dob']
        password = request.form['password']
        new_user = Users(username=username, name=name, accttype='Regular', contact=email, dob=dob, location='Not set',
                         password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard', username=username))
    # return redirect(url_for('select_quiz'))
    return render_template('pages/register.html')


@app.route("/<page>")
def notfound(page):
    return render_template('pages/notFound.html')


if __name__ == "__main__":
    app.run(debug=True)
