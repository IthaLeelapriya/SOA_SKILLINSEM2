
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "app-db"),
        database=os.getenv("DB_NAME", "mydb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "password")
    )

@app.route('/api/data')
def get_data():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100)
            )
        """)

        cur.execute(
            "INSERT INTO students (name) VALUES (%s) RETURNING id",
            ("Leela",)
        )

        conn.commit()

        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Database connected successfully!",
            "data": rows
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
