import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///historical_facts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initializing Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'user' or 'admin'

# Facts Model
class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=False) 

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'user_dashboard'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

# User Dashboard
@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html', username=current_user.username)

# Facts Page
@app.route('/facts')
@login_required
def facts():
    all_facts = Fact.query.all()  # Ensure this retrieves a list of Fact objects
    return render_template('facts.html', facts=all_facts)

from sqlalchemy import or_

@app.route('/information', methods=['GET'])
@login_required
def information():
    query = request.args.get('query')
    results = []

    if query:
        results = Information.query.filter(Information.title.ilike(f'%{query}%')).all()
        if not results:
            flash("No information found for your search.", "warning")

    return render_template('information.html', results=results, query=query)

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        # Collect submitted answers
        answers = request.form
        score = 0

        # Fetch correct answers from DB
        conn = sqlite3.connect('instance/historical_facts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, answer FROM quiz")
        correct_answers = {str(row[0]): row[1] for row in cursor.fetchall()}
        conn.close()

        # Compare submitted answers with correct ones
        for q_id, selected_option in answers.items():
            if q_id in correct_answers and selected_option.strip().lower() == correct_answers[q_id].strip().lower():
                score += 1

        return render_template('user/quiz_result.html', score=score, total=len(correct_answers))

    # Load quiz questions if URL contains ?start=true
    show_questions = request.args.get('start') == 'true'
    questions = []
    if show_questions:
        conn = sqlite3.connect('instance/historical_facts.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz")
        questions = cursor.fetchall()
        conn.close()

    return render_template('quiz.html', show_questions=show_questions, questions=questions)

    

@app.route('/user/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    conn = sqlite3.connect('instance/historical_facts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz")
    questions = cursor.fetchall()
    conn.close()

    score = 0
    total = len(questions)

    for q in questions:
        user_answer = request.form.get(f'q{q["id"]}')
        if user_answer == q["answer"]:  # assumes you have a column named 'answer'
            score += 1

    return render_template('user/quiz_result.html', score=score, total=total)


# Admin Dashboard
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('user_dashboard'))
    facts = Fact.query.all()
    return render_template('admin/admin_dashboard.html', username=current_user.username, facts=facts)

# Admin Routes
@app.route('/admin/manage_facts')
@login_required
def manage_facts():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    facts = Fact.query.all()
    return render_template('admin/manage_facts.html', facts=facts)

@app.route('/admin/add_fact', methods=['GET', 'POST'])
@login_required
def add_fact():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        print("Form Data Received:", request.form)  # Debugging

        title = request.form.get('title')
        description = request.form.get('description')

        if not title or not description:
            flash("Title and Description are required!", "danger")
            return redirect(url_for('add_fact'))

        # ✅ Check if the fact already exists
        existing_fact = Fact.query.filter(db.func.lower(Fact.title) == title.lower()).first()
        if existing_fact:
            flash("❌ This fact already exists!", "danger")
            return redirect(url_for('add_fact'))

        # Create and add the new fact
        new_fact = Fact(title=title, description=description)
        db.session.add(new_fact)

        try:
            db.session.commit()
            flash("✅ Fact added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("⚠️ Error adding fact: " + str(e), "danger")
            return redirect(url_for('add_fact'))

        return redirect(url_for('manage_facts'))

    return render_template('admin/add_fact.html')



@app.route('/admin/edit_fact/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_fact(id):
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    fact = Fact.query.get_or_404(id)
    if request.method == 'POST':
        fact.title = request.form['title']
        fact.description = request.form['description']
        db.session.commit()
        flash("Fact updated successfully!", "info")
        return redirect(url_for('manage_facts'))
    return render_template('admin/edit_fact.html', fact=fact)


@app.route('/admin/delete_fact/<int:id>', methods=['POST'])
@login_required
def delete_fact(id):
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    fact = Fact.query.get_or_404(id)
    db.session.delete(fact)
    db.session.commit()
    flash("Fact deleted successfully!", "danger")
    return redirect(url_for('manage_facts'))


@app.route('/admin/manage_information')
@login_required
def manage_information():
    information_list = Information.query.with_entities(
        Information.id, Information.title, Information.details
    ).all()
    return render_template('admin/manage_information.html', information=information_list)  # ✅ Correct variable



@app.route('/admin/add_information', methods=['GET', 'POST'])
@login_required
def add_information():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('manage_information'))

    if request.method == 'POST':
        # Step 1: Get and normalize user input
        new_title = request.form.get('title', '').strip().lower()
        new_details = request.form.get('details', '').strip().lower()

        # Step 2: Get all existing information from DB
        all_info = Information.query.all()

        # Step 3: Compare with each entry (case-insensitive)
        for info in all_info:
            existing_title = info.title.strip().lower()
            existing_details = info.details.strip().lower()

            if new_title == existing_title and new_details == existing_details:
                flash("This information already exists!", "warning")
                return redirect(url_for('add_information'))

        # Step 4: Add info if not duplicate
        info = Information(title=request.form.get('title').strip(), 
                           details=request.form.get('details').strip())
        db.session.add(info)
        db.session.commit()
        flash("Information added successfully!", "success")
        return redirect(url_for('manage_information'))

    return render_template('admin/add_information.html')


@app.route('/admin/edit_information/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_information(id):
    info = Information.query.get_or_404(id)  # ✅ Fetches info based on ID
    
    if request.method == 'POST':
        info.title = request.form['title']
        info.details = request.form['details']  
        db.session.commit()
        flash('Information updated successfully!', 'success')
        return redirect(url_for('manage_information'))  

    return render_template('edit_information.html', info=info)  # ✅ Pass "info" correctly



@app.route('/admin/delete_information/<int:id>', methods=['POST'])
@login_required
def delete_information(id):
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    info = Information.query.get_or_404(id)
    db.session.delete(info)
    db.session.commit()
    flash("Information deleted successfully!", "danger")
    return redirect(url_for('manage_information'))

@app.route('/user/add_fact', methods=['GET', 'POST'])
@login_required
def user_add_fact():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        if not title or not description:
            flash("Title and Description are required!", "danger")
            return redirect(url_for('user_add_fact'))

        # Add the new fact
        new_fact = Fact(title=title, description=description)
        db.session.add(new_fact)
        try:
            db.session.commit()
            flash("Fact submitted successfully!", "success")
        except:
            db.session.rollback()
            flash("Something went wrong. Try again.", "danger")

        return redirect(url_for('facts'))

    return render_template('user/add_fact.html')


@app.route('/admin/manage_quiz', methods=['GET', 'POST'])
@login_required
def manage_quiz():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    questions = Quiz.query.all()
    return render_template('admin/manage_quiz.html', questions=questions)

@app.route('/admin/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        question = request.form['question'].strip()
        option1 = request.form['option1'].strip()
        option2 = request.form['option2'].strip()
        option3 = request.form['option3'].strip()
        answer = request.form['answer'].strip()

        # Normalize the question for duplicate check
        normalized_question = question.lower()

        # Check for duplicate question
        existing_questions = Quiz.query.all()
        for q in existing_questions:
            if q.question.strip().lower() == normalized_question:
                flash("This question already exists!", "warning")
                return redirect(url_for('add_quiz'))

        # If not duplicate, add to database
        new_question = Quiz(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            answer=answer
        )
        db.session.add(new_question)
        db.session.commit()
        flash("Question added!", "success")
        return redirect(url_for('manage_quiz'))

    return render_template('admin/add_quiz.html')

@app.route('/admin/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        quiz.question = request.form['question']
        quiz.option1 = request.form['option1']
        quiz.option2 = request.form['option2']
        quiz.option3 = request.form['option3']
        quiz.answer = request.form['answer']

        db.session.commit()
        flash("Quiz question updated!", "success")
        return redirect(url_for('manage_quiz'))

    return render_template('admin/edit_quiz.html', quiz=quiz)

@app.route('/admin/delete_quiz/<int:quiz_id>')
@login_required
def delete_quiz(quiz_id):
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))

    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash("Question deleted successfully!", "success")
    return redirect(url_for('manage_quiz'))





# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

# Ensure Admin Exists
def create_admin():
    if not User.query.filter_by(username='admin123').first():
        hashed_password = bcrypt.generate_password_hash('adminpass').decode('utf-8')
        db.session.add(User(username='admin123', email="admin@example.com", password=hashed_password, role='admin'))
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)