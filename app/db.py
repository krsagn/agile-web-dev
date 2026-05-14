from datetime import datetime, timezone

from .models import (
    db,
    RegisteredUser,
    Quiz,
    QuizResult,
)


def find_registered_user_by_identifier(identifier):
    return RegisteredUser.query.filter(
        (RegisteredUser.username == identifier) | (RegisteredUser.email == identifier)
    ).first()


def save_registered_user(
    first_name, last_name, email, username, password_hash, terms_read
):
    user = RegisteredUser(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password_hash=password_hash,
        terms_read=terms_read == "yes",
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(user)
    db.session.commit()


def get_all_quizzes():
    return Quiz.query.all()


def add_sample_quizzes():
    if Quiz.query.count() >= 50:
        return

    science_questions = [
        {
            "question": "What is the chemical symbol for gold?",
            "selection_a": "Au",
            "selection_b": "Ag",
            "selection_c": "Fe",
            "selection_d": "Cu",
            "correct_answer": "A",
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "selection_a": "Venus",
            "selection_b": "Mars",
            "selection_c": "Jupiter",
            "selection_d": "Saturn",
            "correct_answer": "B",
        },
        {
            "question": "What is the powerhouse of the cell?",
            "selection_a": "Nucleus",
            "selection_b": "Ribosome",
            "selection_c": "Mitochondria",
            "selection_d": "Endoplasmic Reticulum",
            "correct_answer": "C",
        },
        {
            "question": "What gas do plants absorb from the atmosphere during photosynthesis?",
            "selection_a": "Oxygen",
            "selection_b": "Carbon Dioxide",
            "selection_c": "Nitrogen",
            "selection_d": "Hydrogen",
            "correct_answer": "B",
        },
        {
            "question": "Which element has the atomic number 1?",
            "selection_a": "Helium",
            "selection_b": "Hydrogen",
            "selection_c": "Lithium",
            "selection_d": "Beryllium",
            "correct_answer": "B",
        },
        {
            "question": "What is the speed of light in vacuum?",
            "selection_a": "300,000 km/s",
            "selection_b": "150,000 km/s",
            "selection_c": "450,000 km/s",
            "selection_d": "600,000 km/s",
            "correct_answer": "A",
        },
        {
            "question": "Which organ in the human body produces insulin?",
            "selection_a": "Liver",
            "selection_b": "Pancreas",
            "selection_c": "Kidney",
            "selection_d": "Stomach",
            "correct_answer": "B",
        },
        {
            "question": "What is the most abundant gas in Earth's atmosphere?",
            "selection_a": "Oxygen",
            "selection_b": "Carbon Dioxide",
            "selection_c": "Nitrogen",
            "selection_d": "Argon",
            "correct_answer": "C",
        },
        {
            "question": "Which scientist developed the theory of relativity?",
            "selection_a": "Isaac Newton",
            "selection_b": "Albert Einstein",
            "selection_c": "Galileo Galilei",
            "selection_d": "Stephen Hawking",
            "correct_answer": "B",
        },
        {
            "question": "What is the pH of pure water?",
            "selection_a": "0",
            "selection_b": "7",
            "selection_c": "14",
            "selection_d": "10",
            "correct_answer": "B",
        },
    ]

    programming_questions = [
        {
            "question": "What does HTML stand for?",
            "selection_a": "Hyper Text Markup Language",
            "selection_b": "High Tech Modern Language",
            "selection_c": "Hyper Transfer Markup Language",
            "selection_d": "Home Tool Markup Language",
            "correct_answer": "A",
        },
        {
            "question": "Which programming language is known as the 'mother of all languages'?",
            "selection_a": "C",
            "selection_b": "Assembly",
            "selection_c": "FORTRAN",
            "selection_d": "COBOL",
            "correct_answer": "C",
        },
        {
            "question": "What is the purpose of CSS?",
            "selection_a": "To structure web content",
            "selection_b": "To style web content",
            "selection_c": "To add interactivity",
            "selection_d": "To store data",
            "correct_answer": "B",
        },
        {
            "question": "Which data structure uses LIFO (Last In, First Out)?",
            "selection_a": "Queue",
            "selection_b": "Stack",
            "selection_c": "Array",
            "selection_d": "Linked List",
            "correct_answer": "B",
        },
        {
            "question": "What does SQL stand for?",
            "selection_a": "Simple Query Language",
            "selection_b": "Structured Query Language",
            "selection_c": "System Query Language",
            "selection_d": "Standard Query Language",
            "correct_answer": "B",
        },
        {
            "question": "Which of these is NOT a programming paradigm?",
            "selection_a": "Object-Oriented",
            "selection_b": "Functional",
            "selection_c": "Procedural",
            "selection_d": "Algorithmic",
            "correct_answer": "D",
        },
        {
            "question": "What is the time complexity of binary search?",
            "selection_a": "O(n)",
            "selection_b": "O(log n)",
            "selection_c": "O(n²)",
            "selection_d": "O(1)",
            "correct_answer": "B",
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "selection_a": "function",
            "selection_b": "def",
            "selection_c": "func",
            "selection_d": "define",
            "correct_answer": "B",
        },
        {
            "question": "What does API stand for?",
            "selection_a": "Application Programming Interface",
            "selection_b": "Advanced Programming Interface",
            "selection_c": "Automated Programming Interface",
            "selection_d": "Application Process Interface",
            "correct_answer": "A",
        },
        {
            "question": "Which sorting algorithm has the best average case time complexity?",
            "selection_a": "Bubble Sort",
            "selection_b": "Insertion Sort",
            "selection_c": "Quick Sort",
            "selection_d": "Selection Sort",
            "correct_answer": "C",
        },
    ]

    geography_questions = [
        {
            "question": "What is the capital of France?",
            "selection_a": "Lyon",
            "selection_b": "Paris",
            "selection_c": "Marseille",
            "selection_d": "Nice",
            "correct_answer": "B",
        },
        {
            "question": "Which country is the largest by land area?",
            "selection_a": "Canada",
            "selection_b": "China",
            "selection_c": "Russia",
            "selection_d": "United States",
            "correct_answer": "C",
        },
        {
            "question": "What is the longest river in the world?",
            "selection_a": "Amazon River",
            "selection_b": "Yangtze River",
            "selection_c": "Nile River",
            "selection_d": "Mississippi River",
            "correct_answer": "C",
        },
        {
            "question": "Which mountain range contains Mount Everest?",
            "selection_a": "Rockies",
            "selection_b": "Alps",
            "selection_c": "Andes",
            "selection_d": "Himalayas",
            "correct_answer": "D",
        },
        {
            "question": "What is the capital of Japan?",
            "selection_a": "Osaka",
            "selection_b": "Tokyo",
            "selection_c": "Kyoto",
            "selection_d": "Yokohama",
            "correct_answer": "B",
        },
        {
            "question": "Which desert is the largest in the world?",
            "selection_a": "Gobi Desert",
            "selection_b": "Sahara Desert",
            "selection_c": "Arabian Desert",
            "selection_d": "Kalahari Desert",
            "correct_answer": "B",
        },
        {
            "question": "What is the capital of Australia?",
            "selection_a": "Sydney",
            "selection_b": "Melbourne",
            "selection_c": "Canberra",
            "selection_d": "Brisbane",
            "correct_answer": "C",
        },
        {
            "question": "Which country has the most islands?",
            "selection_a": "Indonesia",
            "selection_b": "Philippines",
            "selection_c": "Norway",
            "selection_d": "Finland",
            "correct_answer": "A",
        },
        {
            "question": "What is the deepest ocean on Earth?",
            "selection_a": "Atlantic Ocean",
            "selection_b": "Indian Ocean",
            "selection_c": "Arctic Ocean",
            "selection_d": "Pacific Ocean",
            "correct_answer": "D",
        },
        {
            "question": "Which continent is the smallest by land area?",
            "selection_a": "Europe",
            "selection_b": "Australia",
            "selection_c": "Africa",
            "selection_d": "South America",
            "correct_answer": "B",
        },
    ]

    math_questions = [
        {
            "question": "What is the value of π (pi) approximately?",
            "selection_a": "3.14",
            "selection_b": "3.1416",
            "selection_c": "3.14159",
            "selection_d": "3.1415926535",
            "correct_answer": "C",
        },
        {
            "question": "What is the square root of 144?",
            "selection_a": "10",
            "selection_b": "12",
            "selection_c": "14",
            "selection_d": "16",
            "correct_answer": "B",
        },
        {
            "question": "What is 15% of 200?",
            "selection_a": "20",
            "selection_b": "25",
            "selection_c": "30",
            "selection_d": "35",
            "correct_answer": "C",
        },
        {
            "question": "What is the area of a circle with radius 5?",
            "selection_a": "25π",
            "selection_b": "50π",
            "selection_c": "75π",
            "selection_d": "100π",
            "correct_answer": "A",
        },
        {
            "question": "What is 2³?",
            "selection_a": "4",
            "selection_b": "6",
            "selection_c": "8",
            "selection_d": "16",
            "correct_answer": "C",
        },
        {
            "question": "What is the derivative of x²?",
            "selection_a": "x",
            "selection_b": "2x",
            "selection_c": "x²",
            "selection_d": "2",
            "correct_answer": "B",
        },
        {
            "question": "What is the sum of angles in a triangle?",
            "selection_a": "180°",
            "selection_b": "360°",
            "selection_c": "90°",
            "selection_d": "270°",
            "correct_answer": "A",
        },
        {
            "question": "What is log₁₀(100)?",
            "selection_a": "1",
            "selection_b": "2",
            "selection_c": "10",
            "selection_d": "100",
            "correct_answer": "B",
        },
        {
            "question": "What is the factorial of 5?",
            "selection_a": "120",
            "selection_b": "60",
            "selection_c": "24",
            "selection_d": "720",
            "correct_answer": "A",
        },
        {
            "question": "What is the Pythagorean theorem?",
            "selection_a": "a + b = c",
            "selection_b": "a² + b² = c²",
            "selection_c": "a × b = c",
            "selection_d": "a ÷ b = c",
            "correct_answer": "B",
        },
    ]

    biology_questions = [
        {
            "question": "What is the powerhouse of the cell?",
            "selection_a": "Nucleus",
            "selection_b": "Ribosome",
            "selection_c": "Mitochondria",
            "selection_d": "Endoplasmic Reticulum",
            "correct_answer": "C",
        },
        {
            "question": "Which molecule carries genetic information?",
            "selection_a": "Protein",
            "selection_b": "DNA",
            "selection_c": "Carbohydrate",
            "selection_d": "Lipid",
            "correct_answer": "B",
        },
        {
            "question": "What is the process by which plants make their own food?",
            "selection_a": "Respiration",
            "selection_b": "Photosynthesis",
            "selection_c": "Transpiration",
            "selection_d": "Fermentation",
            "correct_answer": "B",
        },
        {
            "question": "Which organelle is responsible for protein synthesis?",
            "selection_a": "Golgi apparatus",
            "selection_b": "Lysosome",
            "selection_c": "Ribosome",
            "selection_d": "Vacuole",
            "correct_answer": "C",
        },
        {
            "question": "What is the basic unit of life?",
            "selection_a": "Atom",
            "selection_b": "Molecule",
            "selection_c": "Cell",
            "selection_d": "Tissue",
            "correct_answer": "C",
        },
        {
            "question": "Which blood cells are responsible for fighting infections?",
            "selection_a": "Red blood cells",
            "selection_b": "White blood cells",
            "selection_c": "Platelets",
            "selection_d": "Plasma",
            "correct_answer": "B",
        },
        {
            "question": "What is the process of cell division in somatic cells called?",
            "selection_a": "Meiosis",
            "selection_b": "Mitosis",
            "selection_c": "Binary fission",
            "selection_d": "Budding",
            "correct_answer": "B",
        },
        {
            "question": "Which vitamin is produced by the skin when exposed to sunlight?",
            "selection_a": "Vitamin A",
            "selection_b": "Vitamin B",
            "selection_c": "Vitamin C",
            "selection_d": "Vitamin D",
            "correct_answer": "D",
        },
        {
            "question": "What is the largest organ in the human body?",
            "selection_a": "Heart",
            "selection_b": "Liver",
            "selection_c": "Skin",
            "selection_d": "Brain",
            "correct_answer": "C",
        },
        {
            "question": "Which type of blood vessel carries blood away from the heart?",
            "selection_a": "Vein",
            "selection_b": "Artery",
            "selection_c": "Capillary",
            "selection_d": "Venule",
            "correct_answer": "B",
        },
    ]

    for q in science_questions:
        db.session.add(Quiz(category="Science", **q))
    for q in programming_questions:
        db.session.add(Quiz(category="Programming", **q))
    for q in math_questions:
        db.session.add(Quiz(category="Math", **q))
    for q in geography_questions:
        db.session.add(Quiz(category="Geography", **q))
    for q in biology_questions:
        db.session.add(Quiz(category="Biology", **q))

    db.session.commit()


def find_registered_user_by_id(user_id):
    return db.session.get(RegisteredUser, user_id)
