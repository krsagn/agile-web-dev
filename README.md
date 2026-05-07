# quokka-app

## About

A web app that gives users a quiz per day across a range of categories. The goal is to make learning a daily habit by keeping sessions short, rewarding consistency, and tracking progress over time.

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

**Leaderboards** - Users can compare scores on a global leaderboard or against friends.

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

There is currently no automated test suite checked into the repository.

When tests are added, run them from the project root after installing the project dependencies:

```bash
python -m pytest
```

If `pytest` is not installed, install it in your active virtual environment first:

```bash
pip install pytest
```
