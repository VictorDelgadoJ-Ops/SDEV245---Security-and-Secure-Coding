"""A03: Injection.

Original problem: concatenating the username into SQL allowed input to alter
the meaning of the query.
Change made: I used a placeholder for the username and passed it separately
to the query. This keeps the input from being treated as SQL code.
"""

def find_user(connection, username):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()