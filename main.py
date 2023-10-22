from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, EmailField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, InputRequired
from werkzeug.security import check_password_hash

from PyPDF2.errors import PdfReadError
from functions import extract_text, user_exists, hash_password, get_quiz, get_today_date

app = Flask(__name__)
app.secret_key = b'secret_key_1004'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindspark.db'
app.config['SQLALCHEMY_BINDS'] = {'mindspark': 'sqlite:///mindspark.db'}
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


class MyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = EmailField('Email Id', validators=[InputRequired()])
    dob = DateField('Date of birth', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min('6'))])
    quiz_title = StringField('Details', validators=[InputRequired()])
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
    acct_plan = db.Column(db.String(50), nullable=False)
    acct_type = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        column_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return column_dict


class Questions(db.Model):
    __bind_key__ = 'mindspark'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    questions = db.Column(db.String(200), nullable=False)
    options = db.Column(db.String(200), nullable=False)
    privacy = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        column_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return column_dict

    def __init__(self, author, name, category, desc, subject, question_type, questions, options, privacy):
        self.author = author
        self.name = name
        self.category = category
        self.desc = desc
        self.subject = subject
        self.question_type = question_type
        self.questions = questions
        self.options = options
        self.privacy = privacy


class Notifications(db.Model):
    __bind_key__ = 'mindspark'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(50), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(50), nullable=False)
    send_date = db.Column(db.String(50), nullable=True)
    send_time = db.Column(db.String(200), nullable=True)


class Support(db.Model):
    __bind_key__ = 'mindspark'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(200), nullable=True)
    reply_date = db.Column(db.String(50), nullable=True)
    reply_user = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        column_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return column_dict

    def __init__(self, username, email, title, msg, status, type, response, reply_date, reply_user):
        self.username = username
        self.email = email
        self.title = title
        self.msg = msg
        self.type = type
        self.status = status
        self.response = response
        self.reply_date = reply_date
        self.reply_user = reply_user


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/add-feedback/<int:user_id>', methods=['GET', 'POST'])
def add_feedback(user_id):
    if request.method == 'POST':
        msg = request.form['msg']
        feedback_question = db.get_or_404(Support, user_id)
        feedback_question.msg = msg
        feedback_question.status = 'replied'
        db.session.commit()
        return redirect(url_for('feedback_page'))


@app.route('/api')
def api():
    all_questions_file = db.session.execute(db.select(Questions).order_by(Questions.id)).fetchall()
    # all_cafe = [Questions.to_dict(cafe[0]) for cafe in all_questions_file]
    all_questions = [Questions.to_dict(questions[0]) for questions in all_questions_file]
    return jsonify(all_questions)


@app.route('/coming-soon')
def coming_soon():
    return render_template('pages/coming_soon.html')


@app.route('/community')
def community():
    return render_template('pages/community.html')


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
        privacy = request.form['privacy']
        try:
            question_text = extract_text(request.files['question-input'])
            option_text = extract_text(request.files['answer-input'])
            new_question = Questions(current_user.username, title, category, desc, subject, question_type,
                                     question_text, option_text, privacy)
            db.session.add(new_question)
            db.session.commit()
        except PdfReadError:  # Correctly catch the PdfReadError
            return render_template('pages/create-quiz.html', form=form, message='FileError, please try again')
        else:
            return render_template('pages/create-quiz.html', form=form,
                                   message_200='Quiz Successfully created!')
    return render_template('pages/create-quiz.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html')


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
    return redirect(url_for('profile', username=current_user.username))


@app.route('/downgrade-user-plan/<int:user_id>', methods=['GET', 'POST'])
@login_required
def downgrade_user_plan(user_id):
    user = db.get_or_404(Users, user_id)
    if user:
        user.acct_plan = 'regular'
        db.session.commit()
    return redirect(url_for('users_page'))


@app.route('/downgrade-user-type/<int:user_id>', methods=['GET', 'POST'])
@login_required
def downgrade_user_type(user_id):
    user = db.get_or_404(Users, user_id)
    if user:
        user.acct_type = 'user'
        db.session.commit()
    return redirect(url_for('users_page'))


@app.route('/endquiz')
@login_required
def endquiz():
    return render_template('pages/endquiz.html')


@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        username = current_user.username
        title = request.form['title']
        msg = request.form['msg']
        email = request.form['email']
        support_type = 'feedback'
        new_support = Support(username=username, email=email, title=title, msg=msg, type=support_type,
                              status='pending', response='--', reply_date='--', reply_user='--')
        db.session.add(new_support)
        db.session.commit()
    return render_template('pages/feedback.html')


@app.route('/feedback-page')
@login_required
def feedback_page():
    all_feedback_file = db.session.execute(db.select(Support).order_by(Support.id)).fetchall()
    all_feedback = [Support.to_dict(support_feedback[0]) for support_feedback in all_feedback_file]
    return render_template('dashboard/feedback.html', all_feedback=all_feedback)


@app.route('/gpa')
@login_required
def gpa():
    return render_template('pages/cgpa.html')


@app.route('/help')
def help_page():
    return render_template('pages/help.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = MyForm()
        if request.method == 'POST':
            email = request.form['email'].lower()
            password = request.form['password']
            next_page = request.args.get('next')
            if next_page:
                next_page = request.args.get('next').replace('/', '')

            try:
                # Validator 2 - Email
                if not email:
                    raise ValueError("Please enter a valid email")

                username = email.split('@')[0]

                # Validator 3 - Existing User
                user = Users.query.filter_by(email=email).first()
                if not user:
                    raise ValueError("Sorry we couldn't find an account with that email")

                if not check_password_hash(user.password, password):
                    raise ValueError("Your password is incorrect!")

                login_user(user)
                # return redirect(url_for(next=request.endpoint))
                return redirect(url_for(next_page or 'index'))
                # return redirect(url_for("dashboard", next_page=next_page, username=username))

            except ValueError as e:
                return render_template('pages/login.html', form=form, message=str(e))
            except Exception as e:
                return render_template('pages/login.html', form=form,
                                       message="An error has occurred. Please check your details and try again")
            # An error has occurred. Please check your details and try again

        return render_template('pages/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<username>')
@login_required
def profile(username):
    # user_quizzes = db.session.execute(db.Select(Questions).filter_by(author=username)).scalars()
    user_quizzes = db.session.query(Questions).filter_by(author=username).all()
    user = Users.query.filter_by(username=username).first_or_404(description="No user with the provided username")
    return render_template('pages/profile.html', user=user, quizzes=user_quizzes)


@app.route('/questions')
@login_required
def questions_page():
    all_questions_raw = db.session.execute(db.select(Questions).order_by(Questions.id)).fetchall()
    all_questions = [Questions.to_dict(question[0]) for question in all_questions_raw]
    return render_template('dashboard/questions.html', all_questions=all_questions)


@app.route('/quiz')
@login_required
def quiz():
    return render_template('pages/quiz.html')


@app.route('/quiz-info/<subject>')
@login_required
def quiz_info(subject):
    all_quiz = db.session.execute(db.select(Questions).order_by(Questions.id)).scalars()
    return render_template('pages/quiz_info.html', all_quiz=all_quiz, subject=subject)


@app.route('/materials')
@login_required
def materials():
    all_questions_raw = db.session.execute(db.select(Questions).order_by(Questions.id)).fetchall()
    all_questions = [Questions.to_dict(question[0]) for question in all_questions_raw]
    return render_template('dashboard/materials.html', all_questions=all_questions)


@app.route("/notfound")
def notfound():
    return render_template('pages/notFound.html')


@app.route("/notifications")
def notifications():
    return render_template('dashboard/notifications.html')


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
        today_date = get_today_date()
        password = request.form['password']
        hashed_password = hash_password(password)
        if user_exists(email, db, Users):
            return render_template('pages/register.html', form=form,
                                   message="An account with the given email already exists!")
        elif not user_exists(username, db, Users):
            new_user = Users(username=username, name=name, acct_plan='regular', acct_type='user', email=email, dob=dob,
                             location='Not set',
                             password=hashed_password, date_joined=today_date)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        else:
            return render_template('pages/register.html', form=form, message="There was an error with your form")
    return render_template('pages/register.html', form=form)


@app.route('/select-quiz/<int:quiz_id>')
@login_required
def select_quiz(quiz_id):
    selected_quiz = db.get_or_404(Questions, quiz_id)
    # all_quiz = db.session.execute(db.select(Questions).order_by(Questions.id)).scalars()
    return render_template('pages/select_quiz.html', quiz=selected_quiz)


@app.route('/support')
@login_required
def support():
    all_feedback_file = db.session.execute(db.select(Support).order_by(Support.id)).fetchall()
    all_support = [Support.to_dict(support_feedback[0]) for support_feedback in all_feedback_file]
    return render_template('dashboard/support.html', all_support=all_support)


@app.route('/support-page', methods=['GET', 'POST'])
@login_required
def support_page():
    if request.method == 'POST':
        username = current_user.username
        title = request.form['title']
        msg = request.form['msg']
        email = request.form['email']
        support_type = 'support'
        new_support = Support(username=username, email=email, title=title, msg=msg, type=support_type,
                              status='pending', response='--', reply_date='--', reply_user='--')
        db.session.add(new_support)
        db.session.commit()
    return render_template('pages/feedback.html')


@app.route('/take-quiz', methods=['GET', 'POST'])
@login_required
def take_quiz():
    amount = request.form['amount']
    if not amount or int(amount) < 1:
        return redirect(url_for('notfound', page='notfound'))
    else:
        # quiz_type = request.form['type']
        quiz_data = get_quiz(amount)
        return render_template('pages/take-quiz.html', quiz_data=quiz_data, quiz_contents=amount)


@app.route('/upgrade-user-plan/<int:user_id>', methods=['GET', 'POST'])
@login_required
def upgrade_user_plan(user_id):
    user = db.get_or_404(Users, user_id)
    if user:
        user.acct_plan = 'premium'
        db.session.commit()
    return redirect(url_for('users_page'))


@app.route('/upgrade-user-type/<int:user_id>', methods=['GET', 'POST'])
@login_required
def upgrade_user_type(user_id):
    user = db.get_or_404(Users, user_id)
    if user:
        user.acct_type = 'moderator'
        db.session.commit()
    return redirect(url_for('users_page'))


@app.route('/users-page')
@login_required
def users_page():
    if current_user.acct_type == 'moderator':
        all_users_raw = db.session.execute(db.select(Users).order_by(Users.id)).fetchall()
        all_users = [Users.to_dict(user[0]) for user in all_users_raw]
        return render_template('dashboard/users.html', all_users=all_users)
    else:
        return redirect(url_for('notfound'))


if __name__ == "__main__":
    app.run(debug=True)

# python_is_cool
