from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

#Flask starter code
from flask import Flask

app = Flask(__name__)
def get_db():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json  

    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (data['amount'], data['category'], data['date'])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added!"}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = get_db()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    result = [dict(row) for row in expenses]  
    return jsonify(result)

@app.route('/summary', methods=['GET'])
def summary():
    conn = get_db()
    data = conn.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
    ''').fetchall()
    result = [dict(row) for row in data]
    return jsonify(result)


@app.route('/')
def home():
    return "Expense Tracker API is running!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

