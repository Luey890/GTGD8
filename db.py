import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect("C:\\Users\\hhmin\\OneDrive\\Documents\\GTGD8\\github\\.database\\gtg.db")
    db.row_factory = sqlite3.Row

    return db

def GetAllGuesses():
    db = GetDB()
    Guesses = db.execute("SELECT * FROM Guesses").fetchall()
    db.close()
    return Guesses

def CheckLogin(username, password):

    db = GetDB()

    # Ask the database for a single user matching the provided name
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()

    # Do they exist?
    if user is not None:
        # OK they exist, is their password correct
        if check_password_hash(user['password'], password):
            # They got it right, return their details 
            return user
        
    # If we get here, the username or password failed.
    return None
