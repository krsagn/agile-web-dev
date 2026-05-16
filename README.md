# quokka-app

## About

Quokka is a web app that gives users a quiz per day across a range of categories. The goal is to make learning a daily habit by keeping sessions short, rewarding consistency, and tracking progress over time.

### How It Works

The user opens the app and is presented with "Today's Quiz". After answering the questions, they receive their score along with explanations for each answer. Progress is saved automatically.

### Categories

- Programming
- General knowledge
- Maths
- Cybersecurity
- Movies and TV
- Science

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
- Responsive CSS breakpoints so the Quokka and grass artwork scale or crop cleanly on smaller screens.

The current visual assets live in `app/static/img/`:

- `quokka-login.png`
- `quokka-grass-floor.png`
- `quokka-register-adventure.png`

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
python -m venv .venv
source .venv/bin/activate

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

### Start the server

```bash
python run.py
```

The Flask development server will start at `http://127.0.0.1:5003`.

| Route       | Description          |
| ----------- | -------------------- |
| `/`         | Home page            |
| `/home`     | Test/reference page  |
| `/login`    | Login page           |
| `/register` | Registration page    |
| `/terms`    | Terms page           |
| `/quiz`     | Quiz page            |
| `/profile`  | User profile page    |
| `/results`  | Quiz results page    |

---

## Running the Tests

The project uses Python's built-in `unittest` framework and has two test suites:

- **Unit tests** — fast tests that exercise models, helpers, and route logic against an in-memory SQLite database via a dedicated `TestingConfig`. They do not touch your dev database.
- **Selenium tests** — end-to-end browser tests in [tests/test_selenium.py](tests/test_selenium.py) that drive a headless Chrome browser against a live Flask server running in a background thread.

### Unit tests only

From the project root, with dependencies installed:

```bash
python -m unittest discover tests -p "test_*.py" -v
```

To skip the Selenium suite (for example, on a machine without Chrome installed), exclude it explicitly:

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
