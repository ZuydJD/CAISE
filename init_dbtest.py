import sqlite3

# Connect to the database
connection = sqlite3.connect('reviews.db')

# Execute the schema file (assuming it contains the schema for `courses` and `reviews`)
with open('courseschema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert some sample data into the `courses` table
cur.execute("INSERT INTO courses (name) VALUES (?)", ('Course 1',))
cur.execute("INSERT INTO courses (name) VALUES (?)", ('Course 2',))
cur.execute("INSERT INTO courses (name) VALUES (?)", ('Course 3',))

# Insert reviews into the `reviews` table
cur.execute("INSERT INTO reviews (course_id, title, content, score) VALUES (?, ?, ?, ?)",
            (1, 'Great Course!', 'I really enjoyed the content and teaching style.', 9)
            )

cur.execute("INSERT INTO reviews (course_id, title, content, score) VALUES (?, ?, ?, ?)",
            (2, 'Good Introduction', 'This course provides a solid foundation.', 8)
            )

# Commit the transaction
connection.commit()

# Close the connection
connection.close()
