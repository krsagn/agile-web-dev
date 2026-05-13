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
from flask_login import current_user, login_required, login_user, logout_user
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from .constants import ACHIEVEMENTS, LEVEL_TITLES, XP_PER_LEVEL
from .db import (
    db,
    find_registered_user_by_id,
    find_registered_user_by_identifier,
    save_registered_user,
    get_all_quizzes,
    add_sample_quizzes,
    Quiz,
    QuizResult,
)
from .models import RegisteredUser, UserAchievement

main = Blueprint("main", __name__)

# Requires GOOGLE_CLIENT_ID in .env (see Discord for setup instructions)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")


def _calculate_level(xp):
    level = 1
    for candidate_level, required_xp in sorted(XP_PER_LEVEL.items()):
        if xp >= required_xp:
            level = candidate_level
    return level


def _next_level_xp(level):
    higher_levels = [
        required_xp
        for candidate_level, required_xp in sorted(XP_PER_LEVEL.items())
        if candidate_level > level
    ]
    if higher_levels:
        return higher_levels[0]
    return XP_PER_LEVEL.get(level, 0)


def _update_user_progress(user, correct_count):
    now = datetime.now(timezone.utc)
    today = now.date()

    if user.last_active is None:
        user.streak = 1
    else:
        last_active = user.last_active
        if last_active.tzinfo is None:
            last_active = last_active.replace(tzinfo=timezone.utc)

        days_since_last_quiz = (today - last_active.date()).days
        if days_since_last_quiz == 1:
            user.streak += 1
        elif days_since_last_quiz > 1:
            user.streak = 1

    user.last_active = now
    user.xp += correct_count * 10
    user.level = _calculate_level(user.xp)


def _achievement_unlocked(key, user, result, correct_answers):
    is_perfect = result.total > 0 and result.score == result.total
    category = result.category.lower()

    rules = {
        "first_quiz": len(user.quiz_results) >= 1,
        "perfect_score": is_perfect,
        "speed_demon": result.time_taken <= 120,
        "streak_7": user.streak >= 7,
        "streak_30": user.streak >= 30,
        "science_ace": category == "science" and is_perfect,
        "code_master": category == "programming" and is_perfect,
        "math_genius": category == "math" and is_perfect,
        "hundred_correct": correct_answers >= 100,
    }

    return rules.get(key, False)


def _unlock_achievements(user, result):
    earned_keys = {achievement.achievement_key for achievement in user.achievements}
    correct_answers = sum(quiz_result.score for quiz_result in user.quiz_results)
    newly_unlocked = []

    for key, definition in ACHIEVEMENTS.items():
        if key in earned_keys:
            continue
        if not _achievement_unlocked(key, user, result, correct_answers):
            continue

        user.achievements.append(
            UserAchievement(
                achievement_key=key,
                earned_at=datetime.now(timezone.utc),
            )
        )
        newly_unlocked.append({"key": key, **definition})

    return newly_unlocked


def _achievement_cards_for(user):
    earned = {
        achievement.achievement_key: achievement.earned_at
        for achievement in user.achievements
    }

    return [
        {
            "key": key,
            **definition,
            "earned": key in earned,
            "earned_at": earned.get(key),
        }
        for key, definition in ACHIEVEMENTS.items()
    ]


@main.route('/')
def index():
    return redirect(url_for('main.login'))


@main.route('/home')
def test():
    return render_template('test-page.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

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

        login_user(user, remember=bool(request.form.get("remember")))
        flash('Logged in successfully.', 'success')
        next_page = request.form.get('next') or request.args.get('next')
        if next_page and next_page.startswith('/') and not next_page.startswith('//'):
            return redirect(next_page)
        return redirect(url_for('main.profile'))

    return render_template("login.html", google_client_id=GOOGLE_CLIENT_ID)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))


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
@login_required
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
    newly_unlocked = []
    if current_user.is_authenticated:
        result = QuizResult(
            user_id=current_user.id,
            category=category or "General",
            score=correct_count,
            total=len(quizzes),
            time_taken=time_taken,
            completed_at=datetime.now(timezone.utc),
        )
        db.session.add(result)
        _update_user_progress(current_user, correct_count)
        db.session.flush()
        newly_unlocked = _unlock_achievements(current_user, result)
        db.session.commit()

    # Store results in session for results page
    session["quiz_results"] = {
        "score": correct_count,
        "total": len(quizzes),
        "percentage": (correct_count / len(quizzes) * 100) if quizzes else 0,
        "time_taken": time_taken,
        "category": category,
        "details": results,
        "new_achievements": newly_unlocked,
    }

    return jsonify({'success': True, 'score': correct_count, 'total': len(quizzes)})


@main.route('/profile')
@login_required
def profile():
    user = find_registered_user_by_id(current_user.id)

    if user is None:
        logout_user()
        flash('User account not found. Please log in again.', 'warning')
        return redirect(url_for('main.login'))

    next_level_xp = _next_level_xp(user.level)
    current_level_xp = XP_PER_LEVEL.get(user.level, 0)
    level_span = max(next_level_xp - current_level_xp, 1)
    best_score = max((r.score for r in user.quiz_results), default=0)
    correct_answers = sum(r.score for r in user.quiz_results)

    profile_data = {
        'full_name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'email': user.email,
        'level': user.level,
        'title': LEVEL_TITLES.get(user.level, 'Quokka Legend'),
        'xp': user.xp,
        'next_level_xp': next_level_xp,
        'xp_percent': max(
            min(round((user.xp - current_level_xp) / level_span * 100), 100),
            0,
        ),
        'streak': user.streak,
        'quiz_wins': len(user.quiz_results),
        'best_score': best_score,
        'correct_answers': correct_answers,
    }

    achievements = _achievement_cards_for(user)

    return render_template(
        'userProfile.html',
        profile=profile_data,
        achievements=achievements,
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


@main.route('/api/history')
@login_required
def get_history():
    results = (
        QuizResult.query
        .filter_by(user_id=current_user.id)
        .order_by(QuizResult.completed_at.desc())
        .all()
    )

    history = [
        {
            'category': result.category,
            'score': result.score,
            'total': result.total,
            'time_taken': result.time_taken,
            'completed_at': result.completed_at.isoformat(),
        }
        for result in results
    ]

    return jsonify({'history': history})

  
@main.route('/api/leaderboard')
def get_leaderboard():
    today = datetime.now(timezone.utc).date()
    current_user_id = current_user.id if current_user.is_authenticated else None

    # Today's scores — best score per user, tiebreak by fastest time
    today_results = (
        db.session.query(QuizResult, RegisteredUser)
        .join(RegisteredUser, QuizResult.user_id == RegisteredUser.id)
        .filter(func.date(QuizResult.completed_at) == today)
        .order_by(QuizResult.score.desc(), QuizResult.time_taken.asc())
        .all()
    )

    seen = set()
    today_list = []
    for result, user in today_results:
        if user.id in seen:
            continue
        seen.add(user.id)
        today_list.append(
            {
                'username': user.username,
                'score': result.score,
                'total': result.total,
                'time_taken': result.time_taken,
                'streak': user.streak,
                'is_current_user': user.id == current_user_id,
            }
        )

    # All-time XP, sorted by XP descending
    quiz_counts = dict(
        db.session.query(QuizResult.user_id, func.count(QuizResult.id))
        .group_by(QuizResult.user_id)
        .all()
    )
    alltime_users = RegisteredUser.query.order_by(RegisteredUser.xp.desc()).all()
    alltime_list = [
        {
            'username': user.username,
            'xp': user.xp,
            'streak': user.streak,
            'quiz_count': quiz_counts.get(user.id, 0),
            'is_current_user': user.id == current_user_id,
        }
        for user in alltime_users
    ]

    return jsonify({'today': today_list, 'all_time': alltime_list})
