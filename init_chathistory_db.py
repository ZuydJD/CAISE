import sqlite3

# Connect to the chat history database
connection = sqlite3.connect('database.db')

# Open the SQL schema for chat history and execute it to create the table
with open('chathistoryschema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert sample chat history data
cur.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)",
            ('user', 'Hello, this is the first message from the user.')
            )

cur.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)",
            ('assistant', 'Hello! How can I assist you today?')
            )

# Commit the changes and close the connection
connection.commit()
connection.close()
