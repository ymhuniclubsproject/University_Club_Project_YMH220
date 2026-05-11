# Backend Preparation Checklist & Guide

## 1. Python Project Structure Starter (Flask)

For a solid API-First Flask backend, we recommend the following professional structure:

```
UniClub/
│
├── app/
│   ├── __init__.py        # Flask app factory (create_app)
│   ├── config.py          # Environment settings/keys
│   ├── models.py          # SQLAlchemy models (users, clubs, events, user_points)
│   ├── schemas.py         # Marshmallow or Pydantic validation schemas
│   ├── extensions.py      # SQLAlchemy, CORS, and JWTManager initializations
│   └── api/
│       ├── __init__.py
│       ├── auth.py        # /api/v1/auth routes
│       ├── clubs.py       # /api/v1/clubs routes
│       ├── events.py      # /api/v1/events routes
│       └── points.py      # /api/v1/users/<id>/points routes
│
├── requirements.txt
├── run.py                 # Entry point (app.run)
└── .env                   # Secrets (DO NOT COMMIT)
```

## 2. CORS Enabled

CORS is crucial so the frontend can retrieve data from the backend without encountering `Cross-Origin Request Blocked` errors. 

**Using Flask:**
```python
pip install flask-cors
```
```python
# In your app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS globally
    return app
```

## 3. SQLite Database Check & Instructions

SQLite comes pre-installed with Python natively—you do not need to install an external database engine! It simply creates a local `.db` file in your repository.

**How to verify / use it:**
In Flask, using **Flask-SQLAlchemy**, this is the setup flow:

1. **Install requirements:**
   `pip install Flask-SQLAlchemy`

2. **Configure app to use SQLite:**
   ```python
   # config.py
   import os
   basedir = os.path.abspath(os.path.dirname(__file__))
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'uniclub.db')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

3. **Initialize the database (Run once):**
   ```python
   # In terminal:
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```
   This command creates the `uniclub.db` file automatically.

## 4. SQLite Schema Implementation Example

```python
# app/models.py
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # ... password hashes, roles, etc.

class Club(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    members = db.Column(db.Integer, default=0)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    quota = db.Column(db.Integer)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'))
    
class UserPoint(db.Model):
    __tablename__ = 'user_points'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200))
```
