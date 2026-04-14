from flask import Flask, request, redirect, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rating INTEGER,
            comments TEXT,
            date_submitted TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HTML TEMPLATES ---------------- #

index_html = """
<!DOCTYPE html>
<html>
<head>
<title>Feedback Form</title>
<style>
body { font-family: Arial; background:#f5f5f5; }
.container { width:60%; margin:auto; background:white; padding:20px; margin-top:40px; border-radius:10px;}
h1,h2 { text-align:center; }
input, select, textarea { width:100%; padding:10px; margin:5px 0; }
button { padding:10px; background:green; color:white; border:none; width:100%; }
a { display:block; text-align:center; margin-top:15px; }
</style>
</head>
<body>
<div class="container">
<h1>Online Feedback System</h1>
<h2>Submit Feedback</h2>

<form action="/submit" method="POST">
<input type="text" name="name" placeholder="Name" required>
<input type="email" name="email" placeholder="Email" required>

<select name="rating">
<option value="1">1 ⭐</option>
<option value="2">2 ⭐</option>
<option value="3">3 ⭐</option>
<option value="4">4 ⭐</option>
<option value="5">5 ⭐</option>
</select>

<textarea name="comments" placeholder="Comments"></textarea>

<button type="submit">Submit</button>
</form>

<a href="/admin">Go to Admin Dashboard</a>
</div>
</body>
</html>
"""

admin_html = """
<!DOCTYPE html>
<html>
<head>
<title>Admin Dashboard</title>
<style>
body { font-family: Arial; background:#f5f5f5; }
.container { width:70%; margin:auto; background:white; padding:20px; margin-top:40px; border-radius:10px;}
h1,h2 { text-align:center; }
table { width:100%; border-collapse:collapse; }
table, th, td { border:1px solid black; padding:10px; text-align:center; }
</style>
</head>
<body>
<div class="container">
<h1>Online Feedback System</h1>
<h2>Admin Dashboard</h2>

<p><b>Total Feedback:</b> {{ total }}</p>
<p><b>Average Rating:</b> {{ avg }}</p>

<table>
<tr>
<th>Name</th>
<th>Email</th>
<th>Rating</th>
<th>Comments</th>
<th>Date</th>
</tr>

{% for row in data %}
<tr>
<td>{{ row[1] }}</td>
<td>{{ row[2] }}</td>
<td>{{ row[3] }}</td>
<td>{{ row[4] }}</td>
<td>{{ row[5] }}</td>
</tr>
{% endfor %}

</table>

<br>
<a href="/">Back to Form</a>
</div>
</body>
</html>
"""

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template_string(index_html)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    comments = request.form['comments']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO feedback (name, email, rating, comments, date_submitted) VALUES (?, ?, ?, ?, ?)",
                (name, email, rating, comments, date))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM feedback")
    data = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM feedback")
    total = cur.fetchone()[0]

    cur.execute("SELECT AVG(rating) FROM feedback")
    avg = cur.fetchone()[0]

    conn.close()

    return render_template_string(admin_html, data=data, total=total, avg=avg)

# Run app
if __name__ == '__main__':
    app.run(debug=True)