from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
conn.commit()

# User Model
class User(BaseModel):
    username: str
    password: str

# Sign-up Route
@app.post("/signup/")
def signup(user: User):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (user.username, user.password))
        conn.commit()
        return {"message": "Account created successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists!")

# Login Route
@app.post("/login/")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (user.username, user.password))
    result = cursor.fetchone()
    if result:
        return {"message": "Login successful!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password!")
