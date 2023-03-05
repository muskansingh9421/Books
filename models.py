import datetime
import sqlite3

conn = sqlite3.connect('book.db')

# # Create the books table
# conn.execute('''CREATE TABLE books
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#               isbn TEXT NOT NULL,
#               title TEXT NOT NULL,
#               author TEXT NOT NULL,
#               year INTEGER NOT NULL)''')

# # Create the users table
# conn.execute('''CREATE TABLE users
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#               username TEXT NOT NULL,
#               password TEXT NOT NULL)''')

# # Create the reviews table
# conn.execute('''CREATE TABLE reviews
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#               rating INTEGER NOT NULL,
#               comment TEXT NOT NULL,
#               posted_on TEXT NOT NULL,
#               book_id INTEGER NOT NULL,
#               user_id INTEGER NOT NULL,
#               FOREIGN KEY(book_id) REFERENCES books(id),
#               FOREIGN KEY(user_id) REFERENCES users(id))''')


# conn.commit()
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')

# cursor.execute("""SELECT rating, comment, posted_on
#                                 FROM reviews
#                                 WHERE book_id = ?""",
#                                 (1,)).fetchall()

# cursor.execute("""INSERT INTO reviews (user_id, book_id, rating, comment, posted_on)
#                                 VALUES (?, ?, ?, ?, ?)""",
#                            (1, 1, "5", "good book", "1/2/2023"))
# conn.commit()

# Execute the SELECT query
# cursor.execute('SELECT rating, comment, posted_on FROM reviews WHERE book_id=?',(1,))

# Fetch all the rows
# rows = cursor.fetchall()

# # Print the rows
# for row in rows:
#     print(row)