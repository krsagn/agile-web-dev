from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class RegisteredUser(UserMixin, db.Model):
    __tablename__ = "registered_users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    terms_read = db.Column(db.Boolean, nullable=False, default=False)
    xp = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=1)
    streak = db.Column(db.Integer, nullable=False, default=0)
    last_active = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

    quiz_results = db.relationship("QuizResult", back_populates="user", lazy=True)
    achievements = db.relationship("UserAchievement", back_populates="user", lazy=True)

    def __getitem__(self, key):
        return getattr(self, key)


class Quiz(db.Model):
    __tablename__ = "quizzes"

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    selection_a = db.Column(db.String, nullable=False)
    selection_b = db.Column(db.String, nullable=False)
    selection_c = db.Column(db.String, nullable=False)
    selection_d = db.Column(db.String, nullable=False)
    correct_answer = db.Column(db.String, nullable=False)


class QuizResult(db.Model):
    __tablename__ = "quiz_results"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("registered_users.id"), nullable=False, index=True
    )
    category = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=False)

    user = db.relationship("RegisteredUser", back_populates="quiz_results")


class UserAchievement(db.Model):
    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("registered_users.id"), nullable=False, index=True
    )
    achievement_key = db.Column(db.String, nullable=False)
    earned_at = db.Column(db.DateTime(timezone=True), nullable=False)

    user = db.relationship("RegisteredUser", back_populates="achievements")
