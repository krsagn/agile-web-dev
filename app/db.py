import os
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, create_engine, or_, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, scoped_session, sessionmaker


class Base(DeclarativeBase):
    pass


class LoginCredential(Base):
    __tablename__ = "login_credentials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RegisteredUser(Base):
    __tablename__ = "registered_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    terms_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __getitem__(self, key):
        return getattr(self, key)


class Quiz(Base):
    __tablename__ = "quizzes"

    question_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    selection_a: Mapped[str] = mapped_column(String, nullable=False)
    selection_b: Mapped[str] = mapped_column(String, nullable=False)
    selection_c: Mapped[str] = mapped_column(String, nullable=False)
    selection_d: Mapped[str] = mapped_column(String, nullable=False)
    correct_answer: Mapped[str] = mapped_column(String, nullable=False)


engine = None
SessionLocal = scoped_session(sessionmaker())


def get_db():
    return SessionLocal()


def close_db(error=None):
    SessionLocal.remove()


def init_db(app):
    global engine

    os.makedirs(app.instance_path, exist_ok=True)
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if database_url is None:
        database_path = app.config["DATABASE"]
        database_url = f"sqlite:///{database_path}"

    engine = create_engine(database_url)
    SessionLocal.configure(bind=engine)
    Base.metadata.create_all(engine)
    app.teardown_appcontext(close_db)


def save_login_credentials(username, password_hash):
    db = get_db()
    credential = LoginCredential(
        username=username,
        password_hash=password_hash,
        created_at=datetime.now(timezone.utc),
    )
    db.add(credential)
    db.commit()


def find_registered_user_by_identifier(identifier):
    db = get_db()
    return db.execute(
        select(RegisteredUser)
        .where(or_(RegisteredUser.username == identifier, RegisteredUser.email == identifier))
        .order_by(RegisteredUser.id.desc())
        .limit(1)
    ).scalar_one_or_none()


def save_registered_user(first_name, last_name, email, username, password_hash, terms_read):
    db = get_db()
    user = RegisteredUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password_hash=password_hash,
        terms_read=terms_read == "yes",
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()


def get_all_quizzes():
    db = get_db()
    return db.execute(select(Quiz)).scalars().all()


def add_sample_quizzes():
    """Add 10 sample quiz questions if they don't exist"""
    db = get_db()
    existing = db.execute(select(Quiz)).scalars().all()
    
    if len(existing) >= 10:
        return  # Already have questions
    
    sample_questions = [
        {
            "question": "What is the primary purpose of the Agile Manifesto?",
            "selection_a": "To define strict rules and procedures for software development",
            "selection_b": "To prioritize individuals and interactions over processes and tools",
            "selection_c": "To replace all documentation with working software",
            "selection_d": "To eliminate the need for any planning in projects",
            "correct_answer": "B"
        },
        {
            "question": "Which of the following is NOT a value in the Agile Manifesto?",
            "selection_a": "Customer collaboration over contract negotiation",
            "selection_b": "Responding to change over following a plan",
            "selection_c": "Comprehensive documentation over working software",
            "selection_d": "Individuals and interactions over processes and tools",
            "correct_answer": "C"
        },
        {
            "question": "What is a Sprint in Agile development?",
            "selection_a": "A final review of the entire project",
            "selection_b": "A fixed time period, usually 1-4 weeks, for completing work",
            "selection_c": "A meeting to discuss future plans",
            "selection_d": "The fastest phase of development",
            "correct_answer": "B"
        },
        {
            "question": "Who is responsible for prioritizing the product backlog?",
            "selection_a": "The Development Team",
            "selection_b": "The Scrum Master",
            "selection_c": "The Product Owner",
            "selection_d": "The Project Manager",
            "correct_answer": "C"
        },
        {
            "question": "What is the main goal of a Daily Standup meeting?",
            "selection_a": "To report to management on project status",
            "selection_b": "To synchronize team activities and identify blockers",
            "selection_c": "To plan the entire sprint",
            "selection_d": "To evaluate team member performance",
            "correct_answer": "B"
        },
        {
            "question": "Which principle is NOT part of the Agile Manifesto?",
            "selection_a": "Deliver working software frequently",
            "selection_b": "Welcome changing requirements",
            "selection_c": "Maximize resource utilization above all else",
            "selection_d": "Business people and developers work together daily",
            "correct_answer": "C"
        },
        {
            "question": "What does 'User Story' represent in Agile?",
            "selection_a": "A document describing system architecture",
            "selection_b": "A brief description of a feature from a user's perspective",
            "selection_c": "A detailed specification of technical requirements",
            "selection_d": "A timeline for project completion",
            "correct_answer": "B"
        },
        {
            "question": "Which Agile framework is most commonly used?",
            "selection_a": "Waterfall",
            "selection_b": "Scrum",
            "selection_c": "Kanban",
            "selection_d": "DevOps",
            "correct_answer": "B"
        },
        {
            "question": "What is the purpose of a Sprint Retrospective?",
            "selection_a": "To review completed work with the client",
            "selection_b": "To plan the next sprint",
            "selection_c": "To reflect on the process and identify improvements",
            "selection_d": "To assign tasks to team members",
            "correct_answer": "C"
        },
        {
            "question": "In Agile, what does 'velocity' refer to?",
            "selection_a": "The speed at which code is written",
            "selection_b": "The amount of work completed in a sprint",
            "selection_c": "The number of bugs fixed per day",
            "selection_d": "The time taken to deploy software",
            "correct_answer": "B"
        }
    ]
    
    for q in sample_questions:
        quiz = Quiz(
            question=q["question"],
            selection_a=q["selection_a"],
            selection_b=q["selection_b"],
            selection_c=q["selection_c"],
            selection_d=q["selection_d"],
            correct_answer=q["correct_answer"]
        )
        db.add(quiz)
    
    db.commit()
