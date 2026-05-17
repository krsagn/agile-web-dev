# quokka-app

## About

Quokka is a web app that gives users a quiz per day across a range of categories. The goal is to make learning a daily habit by keeping sessions short, rewarding consistency, and tracking progress over time.

### How It Works

The user logs in (or registers) and is presented with "Today's Quiz". After answering the questions, they receive their score along with a per-question Answer Review. Progress is saved automatically.

### Categories

- Science
- Programming
- Math
- Geography
- Biology

### Gamification

The app includes several features to keep users engaged over time.

**Streak system** - Users earn a daily streak for completing each quiz. Streaks reset if a day is missed.

**XP and levelling** - Correct answers award XP. Enough XP and the user levels up.

**Achievements** - Milestones are awarded for things like a first perfect score, a 10-day streak, or 100 questions answered.

**Leaderboards** - Users can compare scores on a global leaderboard.

**Email notifications** - Users receive playful Resend-powered emails when they level up, unlock an achievement, or are about to lose a streak (sent daily at 8pm AWST to users with a streak of 2+ who haven't quizzed that day).

### UI and Branding Updates

The project has been rebranded from Daily Quiz to Quokka across the visible app interface.

Recent login and registration page updates include:

- Quokka-themed page titles, brand labels, copy, and terms wording.
- A login page Quokka illustration that peeks from the bottom-right corner and gently reveals more of the character as the user scrolls.
- A responsive grass floor layer on the login page that stays fixed to the bottom of the viewport and animates in after the login layout has been scrolled through.
- A register page Quokka adventure illustration layered over the left side panel with the same soft entrance and idle bob animation style.
- A consistent warm `#f8eedb` page background across the app.
- Animated Quokka artwork on the quiz welcome page, including separate welcome and completed-today states.
- A quiz category page Quokka illustration that rises from the bottom of the main content area toward the category card.
- A sidebar slide-in animation scoped to the quiz welcome page.
- Profile page cards that ease in when the profile loads.
- Responsive CSS breakpoints so the Quokka artwork and grass layer scale or crop cleanly on smaller screens.

The current visual assets live in `app/static/img/`:

- `quokka-login.png`
- `quokka-grass-floor.png`
- `quokka-register-adventure.png`
- `quiz-welcome-glad.png`
- `quiz-welcome-swoop.png`
- `quiz-category-look.png`

---

## Collaborators

| UWA ID   | Name                  | GitHub                                    |
| -------- | --------------------- | ----------------------------------------- |
| 24145866 | Kristian Agena        | [krsagn](https://github.com/krsagn)       |
| 24950379 | Samuel Chiew          | [samuelclw](https://github.com/samuelclw) |
| 24340515 | Kenneth Jones Stephan | [kjonesst](https://github.com/kjonesst)   |
| 24480226 | Zetai Zhang           | [PonKSky234](https://github.com/PonKSky234)       |

---

## Running the App

### Prerequisites

- Python 3.10 or newer
- pip

### Setup

```bash
# From the project root, create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file in the project root with the following keys:

```
SECRET_KEY=<a long random string>
GOOGLE_CLIENT_ID=<your Google OAuth client ID>
RESEND_API_KEY=<your Resend API key>
```

`RESEND_API_KEY` is required for email notifications (level-ups, achievements, streak reminders). Sign up at [resend.com](https://resend.com) for a free key. Without it the app still works — emails just won't send.

To generate a `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Apply database migrations

```bash
flask db upgrade
```

### Seed the database (optional)

To populate the database with a handful of demo users, quiz results, and achievements (useful for poking around the leaderboard and profiles locally):

```bash
flask seed
```

To clear all user data without re-seeding:

```bash
flask reset-db
```

### Start the server

```bash
python run.py
```

The Flask development server will start at `http://127.0.0.1:5003`.

| Route               | Description                  |
| ------------------- | ---------------------------- |
| `/`                 | Home page                    |
| `/login`            | Login page                   |
| `/register`         | Registration page            |
| `/terms`            | Terms page                   |
| `/quiz`             | Quiz welcome page            |
| `/quiz/categories`  | Quiz category selection page |
| `/profile`          | User profile page            |
| `/history`          | Quiz history page            |
| `/leaderboard`      | Leaderboard page             |
| `/users`            | User search page             |
| `/users/<username>` | Public user profile page     |
| `/results`          | Quiz results page            |

---

## Running the Tests

The project uses Python's built-in `unittest` framework and has two test suites:

- **Unit tests** are fast tests that exercise models, helpers, and route logic against an in-memory SQLite database via a dedicated `TestingConfig`. They do not touch your dev database.
- **Selenium tests** in [tests/test_selenium.py](tests/test_selenium.py) drive a headless Chrome browser against a live Flask server running in a background thread.

### Unit tests only

From the project root, with dependencies installed, skip the Selenium suite (for example, on a machine without Chrome installed) by excluding it explicitly:

```bash
python -m unittest discover tests -p "test_[!s]*.py" -v
```

### Selenium tests

The Selenium suite requires:

- Google Chrome installed locally.
- A matching `chromedriver` available on your `PATH`. Recent versions of Selenium (4.6+) include Selenium Manager, which will download a compatible driver automatically the first time the suite runs, so no manual setup is normally required.

Run the Selenium suite on its own with:

```bash
python -m unittest tests.test_selenium -v
```

The suite starts its own Flask server on `localhost:5001`, so make sure that port is free before running. Tests run headlessly by default.

### Running everything

To run the unit tests and the Selenium tests together:

```bash
python -m unittest discover tests -v
```
