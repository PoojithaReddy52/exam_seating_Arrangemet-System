from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from models.database import init_db
from controllers.admin_controller import admin_bp
from controllers.student_controller import student_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['exam_seating_db']

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.role = user_data['role']

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({'_id': user_id})
    if user_data:
        return User(user_data)
    return None

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(student_bp, url_prefix='/student')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.users.find_one({'username': username, 'password': password})
        if user:
            user_obj = User(user)
            login_user(user_obj)
            return redirect(url_for('admin_dashboard' if user['role'] == 'admin' else 'student_dashboard'))
        
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('searchType')
    
    if search_type == 'roll':
        roll_number = request.form.get('rollNumber')
        student = db.students.find_one({'roll_number': roll_number})
        if student:
            arrangements = list(db.arrangements.find({'student_id': student['_id']}))
            return render_template('search_results.html',
                                student=student,
                                arrangements=arrangements)
        flash('Student not found', 'danger')
        
    elif search_type == 'class':
        year = request.form.get('year')
        branch = request.form.get('branch')
        students = list(db.students.find({
            'year': year,
            'branch': branch
        }))
        if students:
            arrangements = []
            for student in students:
                student_arrangements = list(db.arrangements.find({'student_id': student['_id']}))
                arrangements.extend(student_arrangements)
            return render_template('class_results.html',
                                students=students,
                                arrangements=arrangements)
        flash('No students found in this class', 'danger')
        
    elif search_type == 'hall':
        hall_number = request.form.get('hallNumber')
        arrangements = list(db.arrangements.find({'hall_number': hall_number}))
        if arrangements:
            return render_template('hall_results.html',
                                hall_number=hall_number,
                                arrangements=arrangements)
        flash('No arrangements found for this hall', 'danger')
    
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Run the application
    app.run(debug=True) 