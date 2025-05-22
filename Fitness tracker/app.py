from flask import Flask, request, redirect, render_template_string
from collections import Counter
import json

app = Flask(__name__)
workouts = []

# -------- Main Page Template --------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Unbreakable Fitness Tracker</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #d1c4e9, #b3e5fc);
            padding: 20px;
            color: #333;
        }
        h1, h2 {
            text-align: center;
            color: #512da8;
        }
        nav {
            text-align: center;
            margin-bottom: 20px;
        }
        nav a {
            margin: 0 15px;
            text-decoration: none;
            color: #3949ab;
            font-weight: bold;
        }
        form {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
            color: #303f9f;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-top: 5px;
        }
        .checkbox-group {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .checkbox-group label {
            font-weight: normal;
            color: #444;
        }
        button {
            margin-top: 20px;
            width: 100%;
            background-color: #3949ab;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #303f9f;
        }
        table {
            width: 100%;
            margin-top: 40px;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #c5cae9;
            color: #303f9f;
        }
        tr:nth-child(even) {
            background-color: #e8eaf6;
        }
    </style>
</head>
<body>
    <h1>💪 Unbreakable Fitness Tracker 💪</h1>
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/analytics">📊 Analytics</a>
    </nav>
    <form action="/submit" method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" required>

        <label for="date">🗓️ Date:</label>
        <input type="date" name="date" required>

        <label for="exercise">Primary Exercises:</label>
        <div class="checkbox-group">
            <label><input type="checkbox" name="exercise" value="Walking"> 🚶 Walking</label>
            <label><input type="checkbox" name="exercise" value="Running"> 🏃 Running</label>
            <label><input type="checkbox" name="exercise" value="Pushups"> 💪 Pushups</label>
            <label><input type="checkbox" name="exercise" value="Cycling"> 🚴 Cycling</label>
            <label><input type="checkbox" name="exercise" value="Jogging"> 🧍‍♂️ Jogging</label>
        </div>

        <label for="duration">⏱️ Duration (minutes):</label>
        <input type="number" name="duration" placeholder="e.g. 20" required>

        <label for="steps">👣 Steps Count:</label>
        <input type="number" name="steps" placeholder="e.g. 3000">

        <button type="submit">Submit Workout</button>
    </form>

    {% if workouts %}
    <h2>Workout History</h2>
    <table>
        <tr>
            <th>Name</th><th>Date</th><th>Exercises</th><th>Duration</th><th>Steps</th>
        </tr>
        {% for w in workouts %}
        <tr>
            <td>{{ w.name }}</td>
            <td>{{ w.date }}</td>
            <td>{{ w.exercise }}</td>
            <td>{{ w.duration }}</td>
            <td>{{ w.steps }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
'''

# -------- Dashboard Template --------
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Analytics - Unbreakable Fitness Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #f3e5f5, #e1f5fe);
            padding: 30px;
            text-align: center;
        }
        h1 {
            color: #512da8;
        }
        canvas {
            margin-top: 40px;
            max-width: 800px;
            width: 90%;
        }
        .summary {
            margin-top: 20px;
            font-size: 18px;
            color: #333;
        }
        nav {
            margin-bottom: 20px;
        }
        nav a {
            margin: 0 15px;
            text-decoration: none;
            color: #6a1b9a;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>📊 Fitness Analytics Dashboard</h1>
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/analytics">📈 Analytics</a>
    </nav>
    <div class="summary">
        <p>Total Workouts: {{ total_workouts }}</p>
        <p>Total Duration: {{ total_duration }} minutes</p>
        <p>Total Steps: {{ total_steps }}</p>
    </div>
    <canvas id="exerciseChart"></canvas>

    <script>
        const ctx = document.getElementById('exerciseChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ labels | safe }},
                datasets: [{
                    label: 'Exercise Frequency',
                    data: {{ counts | safe }},
                    backgroundColor: '#4dd0e1'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Exercise Frequency' }
                }
            }
        });
    </script>
</body>
</html>
'''

# -------- Routes --------
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, workouts=workouts)

@app.route('/submit', methods=['POST'])
def submit():
    selected_exercises = request.form.getlist('exercise')
    duration = int(request.form['duration'])
    steps = int(request.form.get('steps', 0))

    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'exercise': ', '.join(selected_exercises) if selected_exercises else 'None',
        'duration': f"{duration} minutes",
        'steps': f"{steps} steps" if steps else "—"
    }
    workouts.append(data)
    return redirect('/')

@app.route('/analytics')
def analytics():
    total_workouts = len(workouts)
    total_duration = sum(int(w['duration'].split()[0]) for w in workouts)
    total_steps = sum(int(w['steps'].split()[0]) for w in workouts if w['steps'] != "—")

    all_exercises = []
    for w in workouts:
        all_exercises.extend([e.strip() for e in w['exercise'].split(',') if e.strip()])

    exercise_counts = Counter(all_exercises)
    labels = list(exercise_counts.keys())
    counts = list(exercise_counts.values())

    return render_template_string(DASHBOARD_TEMPLATE,
        total_workouts=total_workouts,
        total_duration=total_duration,
        total_steps=total_steps,
        labels=json.dumps(labels),
        counts=json.dumps(counts)
    )

if __name__ == '__main__':
    app.run(debug=True)
