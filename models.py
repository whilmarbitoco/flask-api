import sqlite3
from faker import Faker

class User:
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')
        self.cursor = self.conn.cursor()

        # self.cursor.execute('''
        # #     CREATE TABLE IF NOT EXISTS users (
        # #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        # #         name TEXT NOT NULL,
        # #         username TEXT UNIQUE NOT NULL,
        # #         password TEXT NOT NULL
        # #     )
        # # ''')
        self.conn.commit()

    def addUser(self, name, username, password):
        try:
            self.cursor.execute('''
                INSERT INTO users (name, username, password)
                VALUES (?, ?, ?)
            ''', (name, username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def getUser(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    def getAllUsers(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def delUser(self, id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        self.conn.commit()
    
    def editUser(self, user_id, name, username, password):
        try:
            self.cursor.execute('''
                UPDATE users
                SET name = ?, username = ?, password = ?
                WHERE id = ?
            ''', (name, username, password, user_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False

    def addRandomData(self, num_entries=10):
        fake = Faker()
        for _ in range(num_entries):
            name = fake.name()
            username = fake.user_name()
            password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

            self.addUser(name, username, password)

    def __del__(self):
        self.conn.close()


