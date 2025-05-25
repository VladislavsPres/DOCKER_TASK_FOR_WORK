from flask import Flask
import psycopg2
import random
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'testdb'),
        user=os.getenv('DB_USER', 'testuser'),
        password=os.getenv('DB_PASS', 'testpass')
    )

@app.route('/addrecord')
def addrecord():
    conn = get_db_connection()
    cur = conn.cursor()
    value = random.randint(1, 1000)
    cur.execute("INSERT INTO records (value) VALUES (%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    return "record added"

@app.route('/deleterecord')
def deleterecord():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE id = (SELECT id FROM records ORDER BY id LIMIT 1)")
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return "record deleted" if affected > 0 else "no records to delete"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)