from flask import Flask, render_template, url_for, request, redirect, jsonify
from get_quiz_t import get_quiz
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, EmailField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired
from werkzeug.security import check_password_hash

from PyPDF2.errors import PdfReadError
from functions import extract_text, user_exists, hash_password

app = Flask(__name__)
app.secret_key = b'secret_key_1004'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_BINDS'] = {'questions': 'sqlite:///questions.db'}
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


class MyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email Id', validators=[InputRequired()])
    dob = DateField('Date of birth', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min('6'))])
    quiz_title = StringField('Quiz Title', validators=[InputRequired()])
    quiz_desc = StringField('Quiz Description', validators=[InputRequired()])
    question_type = SelectField('Question Type', choices=[('', 'Select type'), ('multiple-choice', 'Multiple-choice'),
                                                          ('true/false', 'True/False')], validators=[InputRequired()])
    questions = FileField(validators=[FileRequired()])
    answers = FileField(validators=[FileRequired()])
    subject = SelectField('Subject', validators=[InputRequired()])
    submit = SubmitField('SIGN UP')


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    accttype = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    quiz = db.Column(db.String(500), nullable=True)


class Questions(db.Model):
    __bind_key__ = 'questions'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    questions = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    privacy = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        column_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return column_dict

    def __init__(self, author, name, category, desc, subject, question_type, questions, options, time, privacy):
        self.author = author
        self.name = name
        self.category = category
        self.desc = desc
        self.subject = subject
        self.question_type = question_type
        self.questions = questions
        self.options = options
        self.time = time
        self.privacy = privacy


# with app.app_context():
#     db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/api')
def api():
    all_questions_file = db.session.execute(db.select(Questions).order_by(Questions.id)).fetchall()
    # all_cafe = [Questions.to_dict(cafe[0]) for cafe in all_questions_file]
    all_questions = [Questions.to_dict(questions[0]) for questions in all_questions_file]
    return jsonify(all_questions)


@app.route('/')
def index():
    # return redirect(url_for('select_quiz'))
    return render_template('index.html')


@app.route('/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    form = MyForm()
    if request.method == 'POST':
        title = request.form['quiz_title']
        desc = request.form['quiz_desc']
        subject = request.form['subject']
        question_type = request.form['question_type']
        category = request.form['category']
        time = request.form['time']
        privacy = request.form['privacy']
        try:
            question_text = extract_text(request.files['question-input'])
            option_text = extract_text(request.files['answer-input'])
            new_question = Questions(current_user.username, title, category, desc, subject, question_type,
                                     question_text, option_text, time, privacy)
            db.session.add(new_question)
            db.session.commit()
        except PdfReadError:  # Correctly catch the PdfReadError
            return render_template('pages/create-quiz.html', form=form, message='FileError, please try again')
        else:
            return render_template('pages/create-quiz.html', form=form,
                                   message_200='Quiz Successfully created!')
    return render_template('pages/create-quiz.html', form=form)


@app.route('/coming-soon')
def coming_soon():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/coming_soon.html')


@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    # user_quizzes = db.session.execute(db.Select(Questions).filter_by(author=username)).scalars()
    user_quizzes = db.session.query(Questions).filter_by(author=username).all()
    user = Users.query.filter_by(username=username).first_or_404(description="No user with the provided username")
    return render_template('pages/dashboard.html', user=user, quizzes=user_quizzes)


@app.route('/endquiz')
@login_required
def endquiz():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/endquiz.html')


@app.route('/select-quiz/<int:quiz_id>')
@login_required
def select_quiz(quiz_id):
    selected_quiz = db.get_or_404(Questions, quiz_id)
    # all_quiz = db.session.execute(db.select(Questions).order_by(Questions.id)).scalars()
    return render_template('pages/select_quiz.html', quiz=selected_quiz)


@app.route('/quiz-info/<subject>')
@login_required
def quiz_info(subject):
    all_quiz = db.session.execute(db.select(Questions).order_by(Questions.id)).scalars()
    return render_template('pages/quiz_info.html', all_quiz=all_quiz, subject=subject)


@app.route('/take-quiz', methods=['GET', 'POST'])
@login_required
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
@login_required
def quiz():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/quiz.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()

    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        try:
            # Validator 2 - Email
            if not email:
                raise ValueError("Please enter a valid email")

            username = email.split('@')[0]
            hashed_password = hash_password(password)

            # Validator 3 - Existing User
            user = Users.query.filter_by(contact=email).first()
            if not user:
                raise ValueError("Sorry we couldn't find an account with that email")

            if not check_password_hash(user.password, password):
                raise ValueError("Your password is incorrect!")

            login_user(user)
            return redirect(url_for('dashboard', username=username))

        except ValueError as e:
            return render_template('pages/login.html', form=form, message=str(e))
        except Exception as e:
            return render_template('pages/login.html', form=form,
                                   message="An error has occurred. Please check your details and try again")

    return render_template('pages/login.html', form=form)


@app.route('/recover')
def recover():
    # return redirect(url_for('select_quiz'))
    return render_template('pages/recover.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MyForm()
    if request.method == 'POST':
        email = request.form['email'].lower()
        username = email.split('@')[0]
        name = request.form['name']
        dob = request.form['dob']
        password = request.form['password']
        hashed_password = hash_password(password)
        if user_exists(email, db, Users):
            return render_template('pages/register.html', form=form,
                                   message="An account with the given email already exists!")
        elif not user_exists(username, db, Users):
            new_user = Users(username=username, name=name, accttype='Regular', contact=email, dob=dob,
                             location='Not set',
                             password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('pages/register.html', form=form, message="There was an error with your form")
    return render_template('pages/register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete/<int:acct_id>', methods=['GET', 'POST'])
@login_required
def delete_acct(acct_id):
    user = db.get_or_404(Users, acct_id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/delete_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def delete_quiz(quiz_id):
    quiz_to_delete = db.get_or_404(Questions, quiz_id)
    db.session.delete(quiz_to_delete)
    db.session.commit()
    return redirect(url_for('dashboard', username=current_user.username))


@app.route("/<page>")
def notfound(page):
    return render_template('pages/notFound.html')


if __name__ == "__main__":
    app.run(debug=True)

# python_is_cool
