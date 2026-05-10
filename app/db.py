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
    category: Mapped[str] = mapped_column(String, nullable=False)
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
    """Add sample quiz questions for Science, Programming, and Math categories if they don't exist"""
    db = get_db()
    existing = db.execute(select(Quiz)).scalars().all()
    
    if len(existing) >= 30:  # 10 per category
        return  # Already have questions
    
    science_questions = [
        {
            "question": "What is the chemical symbol for gold?",
            "selection_a": "Au",
            "selection_b": "Ag",
            "selection_c": "Fe",
            "selection_d": "Cu",
            "correct_answer": "A"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "selection_a": "Venus",
            "selection_b": "Mars",
            "selection_c": "Jupiter",
            "selection_d": "Saturn",
            "correct_answer": "B"
        },
        {
            "question": "What is the powerhouse of the cell?",
            "selection_a": "Nucleus",
            "selection_b": "Ribosome",
            "selection_c": "Mitochondria",
            "selection_d": "Endoplasmic Reticulum",
            "correct_answer": "C"
        },
        {
            "question": "What gas do plants absorb from the atmosphere during photosynthesis?",
            "selection_a": "Oxygen",
            "selection_b": "Carbon Dioxide",
            "selection_c": "Nitrogen",
            "selection_d": "Hydrogen",
            "correct_answer": "B"
        },
        {
            "question": "Which element has the atomic number 1?",
            "selection_a": "Helium",
            "selection_b": "Hydrogen",
            "selection_c": "Lithium",
            "selection_d": "Beryllium",
            "correct_answer": "B"
        },
        {
            "question": "What is the speed of light in vacuum?",
            "selection_a": "300,000 km/s",
            "selection_b": "150,000 km/s",
            "selection_c": "450,000 km/s",
            "selection_d": "600,000 km/s",
            "correct_answer": "A"
        },
        {
            "question": "Which organ in the human body produces insulin?",
            "selection_a": "Liver",
            "selection_b": "Pancreas",
            "selection_c": "Kidney",
            "selection_d": "Stomach",
            "correct_answer": "B"
        },
        {
            "question": "What is the most abundant gas in Earth's atmosphere?",
            "selection_a": "Oxygen",
            "selection_b": "Carbon Dioxide",
            "selection_c": "Nitrogen",
            "selection_d": "Argon",
            "correct_answer": "C"
        },
        {
            "question": "Which scientist developed the theory of relativity?",
            "selection_a": "Isaac Newton",
            "selection_b": "Albert Einstein",
            "selection_c": "Galileo Galilei",
            "selection_d": "Stephen Hawking",
            "correct_answer": "B"
        },
        {
            "question": "What is the pH of pure water?",
            "selection_a": "0",
            "selection_b": "7",
            "selection_c": "14",
            "selection_d": "10",
            "correct_answer": "B"
        }
    ]

    programming_questions = [
        {
            "question": "What does HTML stand for?",
            "selection_a": "Hyper Text Markup Language",
            "selection_b": "High Tech Modern Language",
            "selection_c": "Hyper Transfer Markup Language",
            "selection_d": "Home Tool Markup Language",
            "correct_answer": "A"
        },
        {
            "question": "Which programming language is known as the 'mother of all languages'?",
            "selection_a": "C",
            "selection_b": "Assembly",
            "selection_c": "FORTRAN",
            "selection_d": "COBOL",
            "correct_answer": "C"
        },
        {
            "question": "What is the purpose of CSS?",
            "selection_a": "To structure web content",
            "selection_b": "To style web content",
            "selection_c": "To add interactivity",
            "selection_d": "To store data",
            "correct_answer": "B"
        },
        {
            "question": "Which data structure uses LIFO (Last In, First Out)?",
            "selection_a": "Queue",
            "selection_b": "Stack",
            "selection_c": "Array",
            "selection_d": "Linked List",
            "correct_answer": "B"
        },
        {
            "question": "What does SQL stand for?",
            "selection_a": "Simple Query Language",
            "selection_b": "Structured Query Language",
            "selection_c": "System Query Language",
            "selection_d": "Standard Query Language",
            "correct_answer": "B"
        },
        {
            "question": "Which of these is NOT a programming paradigm?",
            "selection_a": "Object-Oriented",
            "selection_b": "Functional",
            "selection_c": "Procedural",
            "selection_d": "Algorithmic",
            "correct_answer": "D"
        },
        {
            "question": "What is the time complexity of binary search?",
            "selection_a": "O(n)",
            "selection_b": "O(log n)",
            "selection_c": "O(n²)",
            "selection_d": "O(1)",
            "correct_answer": "B"
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "selection_a": "function",
            "selection_b": "def",
            "selection_c": "func",
            "selection_d": "define",
            "correct_answer": "B"
        },
        {
            "question": "What does API stand for?",
            "selection_a": "Application Programming Interface",
            "selection_b": "Advanced Programming Interface",
            "selection_c": "Automated Programming Interface",
            "selection_d": "Application Process Interface",
            "correct_answer": "A"
        },
        {
            "question": "Which sorting algorithm has the best average case time complexity?",
            "selection_a": "Bubble Sort",
            "selection_b": "Insertion Sort",
            "selection_c": "Quick Sort",
            "selection_d": "Selection Sort",
            "correct_answer": "C"
        }
    ]

    math_questions = [
        {
            "question": "What is the value of π (pi) approximately?",
            "selection_a": "3.14",
            "selection_b": "3.1416",
            "selection_c": "3.14159",
            "selection_d": "3.1415926535",
            "correct_answer": "C"
        },
        {
            "question": "What is the square root of 144?",
            "selection_a": "10",
            "selection_b": "12",
            "selection_c": "14",
            "selection_d": "16",
            "correct_answer": "B"
        },
        {
            "question": "What is 15% of 200?",
            "selection_a": "20",
            "selection_b": "25",
            "selection_c": "30",
            "selection_d": "35",
            "correct_answer": "C"
        },
        {
            "question": "What is the area of a circle with radius 5?",
            "selection_a": "25π",
            "selection_b": "50π",
            "selection_c": "75π",
            "selection_d": "100π",
            "correct_answer": "A"
        },
        {
            "question": "What is 2³?",
            "selection_a": "4",
            "selection_b": "6",
            "selection_c": "8",
            "selection_d": "16",
            "correct_answer": "C"
        },
        {
            "question": "What is the derivative of x²?",
            "selection_a": "x",
            "selection_b": "2x",
            "selection_c": "x²",
            "selection_d": "2",
            "correct_answer": "B"
        },
        {
            "question": "What is the sum of angles in a triangle?",
            "selection_a": "180°",
            "selection_b": "360°",
            "selection_c": "90°",
            "selection_d": "270°",
            "correct_answer": "A"
        },
        {
            "question": "What is log₁₀(100)?",
            "selection_a": "1",
            "selection_b": "2",
            "selection_c": "10",
            "selection_d": "100",
            "correct_answer": "B"
        },
        {
            "question": "What is the factorial of 5?",
            "selection_a": "120",
            "selection_b": "60",
            "selection_c": "24",
            "selection_d": "720",
            "correct_answer": "A"
        },
        {
            "question": "What is the Pythagorean theorem?",
            "selection_a": "a + b = c",
            "selection_b": "a² + b² = c²",
            "selection_c": "a × b = c",
            "selection_d": "a ÷ b = c",
            "correct_answer": "B"
        }
    ]
    
    for q in science_questions:
        quiz = Quiz(
            category="Science",
            question=q["question"],
            selection_a=q["selection_a"],
            selection_b=q["selection_b"],
            selection_c=q["selection_c"],
            selection_d=q["selection_d"],
            correct_answer=q["correct_answer"]
        )
        db.add(quiz)
    
    for q in programming_questions:
        quiz = Quiz(
            category="Programming",
            question=q["question"],
            selection_a=q["selection_a"],
            selection_b=q["selection_b"],
            selection_c=q["selection_c"],
            selection_d=q["selection_d"],
            correct_answer=q["correct_answer"]
        )
        db.add(quiz)
    
    for q in math_questions:
        quiz = Quiz(
            category="Math",
            question=q["question"],
            selection_a=q["selection_a"],
            selection_b=q["selection_b"],
            selection_c=q["selection_c"],
            selection_d=q["selection_d"],
            correct_answer=q["correct_answer"]
        )
        db.add(quiz)
    
    db.commit()

def find_registered_user_by_id(user_id):
    db = get_db()
    return db.execute(
        select(RegisteredUser)
        .where(RegisteredUser.id == user_id)
        .limit(1)
    ).scalar_one_or_none()