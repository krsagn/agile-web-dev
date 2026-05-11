import os
from datetime import datetime, timezone
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from werkzeug.security import check_password_hash, generate_password_hash

from .db import (
    db,
    find_registered_user_by_id,
    find_registered_user_by_identifier,
    save_login_credentials,
    save_registered_user,
    get_all_quizzes,
    add_sample_quizzes,
    Quiz,
    QuizResult,
)

main = Blueprint("main", __name__)

# Requires GOOGLE_CLIENT_ID in .env (see Discord for setup instructions)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")


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

    return render_template("login.html", google_client_id=GOOGLE_CLIENT_ID)


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

        required_fields = [
            first_name,
            last_name,
            email,
            username,
            password,
            confirm_password,
        ]
        if not all(required_fields):
            flash('Please complete all registration fields.', 'danger')
            return render_template('register.html'), 400

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html'), 400

        if terms_read != 'yes':
            flash(
                'Please read and accept the terms before creating an account.', 'danger'
            )
            return render_template('register.html'), 400

        password_hash = generate_password_hash(password)
        try:
            save_registered_user(
                first_name,
                last_name,
                email,
                username,
                password_hash,
                terms_read,
            )
        except Exception:
            flash("An account with that email or username already exists.", "danger")
            return (
                render_template("register.html", google_client_id=GOOGLE_CLIENT_ID),
                409,
            )
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", google_client_id=GOOGLE_CLIENT_ID)


@main.route('/terms')
def terms():
    return render_template('terms.html')


@main.route('/quiz')
def quiz():
    return render_template('quiz.html')


@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')


@main.route('/history')
def history():
    return render_template('history.html')


@main.route('/api/quizzes')
def get_quizzes():
    # Ensure sample quizzes exist
    add_sample_quizzes()

    category = request.args.get("category")
    if category:
        quizzes = Quiz.query.filter_by(category=category).all()
    else:
        quizzes = get_all_quizzes()

    quiz_list = []
    for quiz in quizzes:
        quiz_list.append(
            {
                'question_id': quiz.question_id,
                'question': quiz.question,
                'options': {
                    'A': quiz.selection_a,
                    'B': quiz.selection_b,
                    'C': quiz.selection_c,
                    'D': quiz.selection_d,
                },
                'correct': quiz.correct_answer,
            }
        )
    return jsonify(quiz_list)


@main.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    user_answers = data.get("answers", {})
    time_taken = data.get("time", 0)
    category = data.get("category")

    if category:
        quizzes = Quiz.query.filter_by(category=category).all()
    else:
        quizzes = get_all_quizzes()

    correct_count = 0
    results = []

    for quiz in quizzes:
        question_id = quiz.question_id
        user_answer = user_answers.get(str(question_id), None)
        is_correct = user_answer == quiz.correct_answer

        if is_correct:
            correct_count += 1

        results.append(
            {
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
                },
            }
        )

    # Persist to DB if user is logged in
    user = session.get("user")
    if user:
        result = QuizResult(
            user_id=user["id"],
            category=category or "General",
            score=correct_count,
            total=len(quizzes),
            time_taken=time_taken,
            completed_at=datetime.now(timezone.utc),
        )
        db.session.add(result)
        db.session.commit()

    # Store results in session for results page
    session["quiz_results"] = {
        "score": correct_count,
        "total": len(quizzes),
        "percentage": (correct_count / len(quizzes) * 100) if quizzes else 0,
        "time_taken": time_taken,
        "category": category,
        "details": results,
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

    next_level_xp = 1000
    best_score = max((r.score for r in user.quiz_results), default=0)
    correct_answers = sum(r.score for r in user.quiz_results)

    profile_data = {
        'full_name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'email': user.email,
        'level': user.level,
        'title': 'New Quokka',  # TODO: derive title from level
        'xp': user.xp,
        'next_level_xp': next_level_xp,  # TODO: compute based on levelling curve
        'xp_percent': min(round(user.xp / next_level_xp * 100), 100),
        'streak': user.streak,
        'quiz_wins': len(user.quiz_results),
        'best_score': best_score,
        'correct_answers': correct_answers,
    }

    achievements = [
        {
            'icon': 'bi-lightning-charge',
            'name': 'Fast Thinker',
            'description': 'Finished a quiz quickly',
        },
        {
            'icon': 'bi-fire',
            'name': 'Streak Master',
            'description': 'Reached a 10 day streak',
        },
        {
            'icon': 'bi-award',
            'name': 'Top Scorer',
            'description': 'Scored above 1000 points',
        },
    ]

    recent_history = session.get('quiz_results')

    return render_template(
        'userProfile.html',
        profile=profile_data,
        achievements=achievements,
        recent_history=recent_history,
    )


@main.route('/results')
def results():
    return render_template('results.html')


@main.route('/api/quiz-results')
def get_quiz_results():
    quiz_results = session.get('quiz_results', None)
    if not quiz_results:
        return jsonify({"quiz_results": None})
    return jsonify({"quiz_results": quiz_results})
