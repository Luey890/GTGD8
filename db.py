#import libraries
import sqlite3
import hashlib
import os

def GetDB():

    # Connect to the database and return the connection object
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Turns the part of the current file into an absolute path and then gets the directory of that path. Used to find the database file regardless of where the program is run from.
    db_path = os.path.join(BASE_DIR, ".database", "gtg.db") #Creates path to the database file 
    db = sqlite3.connect(db_path) 
    db.row_factory = sqlite3.Row

    return db

def GetAllGuesses():

    # Connect, query all guesses and then return the data
    db = GetDB()
    guesses = db.execute("""SELECT Guesses.date, Guesses.show, Guesses.score, Users.username
                            FROM Guesses JOIN Users ON Guesses.user_id = Users.id
                            ORDER BY date DESC""").fetchall()
    db.close()
    return guesses

def CheckLogin(username, password):

    db = GetDB()

    # Ask the database for a single user matching the provided name
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()

    # Do they exist?
    if user is not None:
        user_salt = user['salt'] # Get the salt for this user.

        if user_salt is None:
            hashed_input = hashlib.sha1(password.encode('utf-8')).hexdigest()
            return user if user['password'] == hashed_input else None  
        input_salted = (password + user_salt).encode('utf-8')
        hashed_input = hashlib.sha1(input_salted).hexdigest()
       
        if user['password'] == hashed_input:
            return user
    # If we get here, the username or password failed.
    return None

def RegisterUser(username, password):

    # Check if they gave us a username and password
    if username is None or password is None:
        return False
    salt = os.urandom(16).hex()
    salted_password = (password + salt).encode('utf-8')
    sha1_hash = hashlib.sha1(salted_password).hexdigest()

    # Attempt to add them to the database
    db = GetDB()
    try:
        db.execute("INSERT INTO Users(username, password, salt) VALUES(?, ?, ?)", 
                   (username, sha1_hash, salt))
        db.commit()
        return True
    except sqlite3.Error:
        return False

##################################
### New code starts here
##################################
def AddGuess(user_id, date, game, score):
   
    # Check if any boxes were empty
    if date is None or game is None:
        return False
   
    # Get the DB and add the guess
    db = GetDB()
    db.execute("INSERT INTO Guesses(user_id, date, show, score) VALUES (?, ?, ?, ?)",
               (user_id, date, game, score,))
    db.commit()

    return True
def GetPages(limit, offset):

    #Get the DB and return a page of guesses based on the limit and offset
    db = GetDB()
    query = """SELECT Guesses.date, Guesses.show, Guesses.score, Users.username 
               FROM Guesses 
               JOIN Users ON Guesses.user_id = Users.id 
               ORDER BY date DESC 
               LIMIT ? OFFSET ?"""
    guesses = db.execute(query, (limit, offset)).fetchall()
    db.close()
    return guesses

def TotalGuessCount():
    #Get the DB and return the total number of guesses in the database
    db = GetDB()
    result = db.execute("SELECT COUNT(*) as total FROM Guesses").fetchone()
    db.close()
    return result['total']
