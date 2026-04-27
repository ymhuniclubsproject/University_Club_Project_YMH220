import sqlite3
try:
    conn = sqlite3.connect('uniclub.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA integrity_check')
    print("Integrity check result:", cursor.fetchall())
except Exception as e:
    print("Database Error:", repr(e))
