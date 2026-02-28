# QuoteBot — AI Quote Recommendation Chatbot

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install rasa rasa-sdk
```

## Train

```bash
rasa train
```

## Run

Open **three terminals** inside the project folder (venv activated in each):

**Terminal 1 — Action Server:**
```bash
rasa run actions
```

**Terminal 2 — Rasa Server:**
```bash
rasa run --enable-api --cors "*"
```

**Terminal 3 — Open frontend:**
```
Open frontend/index.html in your browser
```

## Supported Categories

| Trigger phrase          | Category    |
|-------------------------|-------------|
| Give me motivation      | Motivation  |
| Inspire me              | Inspiration |
| Love quote please       | Love        |
| Success quote           | Success     |
| Make me laugh           | Funny       |

## Rasa Version

Tested with **Rasa 3.x** and **rasa-sdk 3.x**
