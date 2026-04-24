# daily-quiz-app

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
| 24480226 | Zetai Zhang           | [ZetaiZ](https://github.com/ZetaiZ)       |

---

## Running the App

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
# Clone the repo, then install dependencies
pip install -r requirements.txt
```

### Start the server

```bash
python run.py
```

The Flask development server will start at `http://127.0.0.1:5001`.

| Route   | Description     |
| ------- | --------------- |
| `/`     | Home page       |
| `/home` | Test/reference page |

---

## Running the Tests

Not yet available.
