import os
from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from werkzeug.security import check_password_hash, generate_password_hash

from .db import find_registered_user_by_identifier, save_login_credentials, save_registered_user, get_all_quizzes, add_sample_quizzes

main = Blueprint('main', __name__)

GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "327860289516-5pnn1vlr17acsttkv8miat03hsl40ahd.apps.googleusercontent.com"
)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def test():
    return render_template('test-page.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash('Please enter both your username/email and password.', 'danger')
            return render_template('login.html'), 400

        user = find_registered_user_by_identifier(identifier)
        if user is None or not check_password_hash(user['password_hash'], password):
            flash('Invalid username/email or password.', 'danger')
            return render_template('login.html'), 401

        save_login_credentials(identifier, generate_password_hash(password))
        session['user'] = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
        }
        flash('Logged in successfully.', 'success')
        return redirect(url_for('main.profile'))

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms_read = request.form.get('terms_read', 'no')

        required_fields = [first_name, last_name, email, username, password, confirm_password]
        if not all(required_fields):
            flash('Please complete all registration fields.', 'danger')
            return render_template('register.html'), 400

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html'), 400

        if terms_read != 'yes':
            flash('Please read and accept the terms before creating an account.', 'danger')
            return render_template('register.html'), 400

        password_hash = generate_password_hash(password)
        save_registered_user(
            first_name,
            last_name,
            email,
            username,
            password_hash,
            terms_read,
        )
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route('/quiz')
def quiz():
    return render_template('quiz.html')

@main.route('/api/quizzes')
def get_quizzes():
    # Ensure sample quizzes exist
    add_sample_quizzes()
    
    quizzes = get_all_quizzes()
    quiz_list = []
    for quiz in quizzes:
        quiz_list.append({
            'question_id': quiz.question_id,
            'question': quiz.question,
            'options': {
                'A': quiz.selection_a,
                'B': quiz.selection_b,
                'C': quiz.selection_c,
                'D': quiz.selection_d,
            },
            'correct': quiz.correct_answer
        })
    return jsonify(quiz_list)

@main.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    user_answers = data.get('answers', {})
    time_taken = data.get('time', 0)
    
    quizzes = get_all_quizzes()
    
    correct_count = 0
    results = []
    
    for quiz in quizzes:
        question_id = quiz.question_id
        user_answer = user_answers.get(str(question_id), None)
        is_correct = user_answer == quiz.correct_answer
        
        if is_correct:
            correct_count += 1
        
        results.append({
            'question_id': question_id,
            'question': quiz.question,
            'user_answer': user_answer,
            'correct_answer': quiz.correct_answer,
            'is_correct': is_correct,
            'options': {
                'A': quiz.selection_a,
                'B': quiz.selection_b,
                'C': quiz.selection_c,
                'D': quiz.selection_d,
            }
        })
    
    # Store results in session
    session['quiz_results'] = {
        'score': correct_count,
        'total': len(quizzes),
        'percentage': (correct_count / len(quizzes) * 100) if quizzes else 0,
        'time_taken': time_taken,
        'details': results
    }
    
    return jsonify({'success': True, 'score': correct_count, 'total': len(quizzes)})

@main.route('/profile')
def profile():
    session_user = session.get('user')

    if not session_user:
        flash('Please log in first.', 'warning')
        return redirect(url_for('main.login'))

    user = find_registered_user_by_id(session_user['id'])

    if user is None:
        session.clear()
        flash('User account not found. Please log in again.', 'warning')
        return redirect(url_for('main.login'))

    profile_data = {
        'full_name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'email': user.email,
        'level': 1,
        'title': 'New Quokka',
        'xp': 0,
        'next_level_xp': 1000,
        'xp_percent': 0,
        'streak': 0,
        'quiz_wins': 0,
        'best_score': 0,
        'correct_answers': 0
    }

    achievements = [
        {
            'icon': 'bi-lightning-charge',
            'name': 'Fast Thinker',
            'description': 'Finished a quiz quickly'
        },
        {
            'icon': 'bi-fire',
            'name': 'Streak Master',
            'description': 'Reached a 10 day streak'
        },
        {
            'icon': 'bi-award',
            'name': 'Top Scorer',
            'description': 'Scored above 1000 points'
        }
    ]

    recent_history = session.get('quiz_results')

    return render_template(
        'userProfile.html',
        profile=profile_data,
        achievements=achievements,
        recent_history=recent_history
    )

@main.route('/results')
def results():
    return render_template('results.html')

@main.route('/api/quiz-results')
def get_quiz_results():
    quiz_results = session.get('quiz_results', None)
    if not quiz_results:
        return jsonify({'quiz_results': None})
    return jsonify({'quiz_results': quiz_results})
