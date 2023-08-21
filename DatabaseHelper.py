import sqlite3
import hashlib

db = sqlite3.connect('database.db')
cursor = db.cursor()

# Create the database for the users
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT, 
        password TEXT,
        gamesPlayed INTEGER,
        gamesWon INTEGER
    )""")


def addUser(username, password):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        return False
    else:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, password, 0, 0))
        db.commit()
        return True


def validateUsernamePassword(username, password):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = cursor.fetchone()
    if user:
        if user[1] == password:
            return True
    return False


def validateUsername(username):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = cursor.fetchone()
    if user:
        return True
    return False


def removeUser(username):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM users WHERE name = ?", (username,))
        db.commit()
        return True
    else:
        return False


def updateStats(username, won):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE users SET gamesPlayed = gamesPlayed + 1 WHERE name = ?", (username,))
        if won:
            cursor.execute("UPDATE users SET gamesWon = gamesWon + 1 WHERE name = ?", (username,))
        db.commit()
        return True
    else:
        return False


def updateUsername(username, newUsername):
    if validateUsername(newUsername):  # Check if new username already exists
        return False
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE users SET name = ?", (newUsername,))
        db.commit()
        return True
    else:
        return False


def getStats(username):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = cursor.fetchone()
    if user:
        return user[2], user[3]
    else:
        return None, None


def updatePassword(username, new_password):
    cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE users SET password = ? WHERE name = ?", (new_password, username))
        db.commit()
        return True
    else:
        return False


def hashPassword(password):
    salt = "1f6"
    return hashlib.md5((password + salt).encode()).hexdigest()


# For debugging purposes
def db_print():
    users = cursor.execute("SELECT * FROM users")
    for user in users:
        print(user)





