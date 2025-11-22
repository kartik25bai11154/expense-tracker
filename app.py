from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    amount REAL,
                    date TEXT
                )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY id DESC")
    data = cur.fetchall()

    # Calculate total spending
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0]
    if total is None:
        total = 0

    conn.close()
    return render_template("index.html", expenses=data, total=total)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        date = request.form["date"]

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (title, amount, date) VALUES (?, ?, ?)",
                    (title, amount, date))
        conn.commit()
        conn.close()
        return redirect("/")
    
    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
