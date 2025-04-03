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

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/information')
@login_required
def information():
    return render_template('information.html')

@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

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
        title = request.form['title']
        description = request.form['description']
        new_fact = Fact(title=title, description=description)
        db.session.add(new_fact)
        db.session.commit()
        flash("Fact added successfully!", "success")
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
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('manage_information.html')
@app.route('/admin/manage_quiz')
@login_required
def manage_quiz():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('manage_quiz.html')

@app.route('/admin/manage_feedback')
@login_required
def manage_feedback():
    if current_user.role != 'admin':
        flash("Unauthorized access!", "danger")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('manage_feedback.html')



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
