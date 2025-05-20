from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

workouts = []

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fitness Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #e0f7fa, #e1bee7);
            padding: 20px;
        }
        h1, h2 {
            text-align: center;
            color: #4a148c;
        }
        form {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            margin-top: 20px;
            width: 100%;
            background-color: #8e24aa;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #6a1b9a;
        }
        table {
            width: 100%;
            margin-top: 40px;
            border-collapse: collapse;
            background: white;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ccc;
            text-align: center;
        }
        th {
            background-color: #ce93d8;
        }
    </style>
</head>
<body>
    <h1>Fitness Tracker</h1>
    <form action="/submit" method="post">
        <label for="name">Name:</label>
        <input type="text" name="name" required>

        <label for="date">Date:</label>
        <input type="date" name="date" required>

        <label for="exercise">Exercise:</label>
        <input type="text" name="exercise" required>

        <label for="duration">Duration (minutes):</label>
        <input type="number" name="duration" required>

        <label for="calories">Calories Burned:</label>
        <input type="number" name="calories" required>

        <label for="activity">Activity Goals:</label>
        <input type="text" name="activity">

        <label for="energy">Energy Burned (kcal):</label>
        <input type="number" name="energy">

        <label for="steps">Steps Count:</label>
        <input type="number" name="steps">

        <label for="exercise_days">Exercise Days (this week):</label>
        <input type="number" name="exercise_days">

        <label for="active_zone">Active Zone Minutes:</label>
        <input type="number" name="active_zone">

        <label for="distance">Distance Travelled (km):</label>
        <input type="number" step="0.01" name="distance">

        <button type="submit">Submit Workout</button>
    </form>

    {% if workouts %}
    <h2>Workout History</h2>
    <table>
        <tr>
            <th>Name</th><th>Date</th><th>Exercise</th><th>Duration</th>
            <th>Calories</th><th>Activity</th><th>Energy</th><th>Steps</th>
            <th>Days</th><th>Zone</th><th>Distance</th>
        </tr>
        {% for w in workouts %}
        <tr>
            <td>{{ w.name }}</td>
            <td>{{ w.date }}</td>
            <td>{{ w.exercise }}</td>
            <td>{{ w.duration }}</td>
            <td>{{ w.calories }}</td>
            <td>{{ w.activity }}</td>
            <td>{{ w.energy }}</td>
            <td>{{ w.steps }}</td>
            <td>{{ w.exercise_days }}</td>
            <td>{{ w.active_zone }}</td>
            <td>{{ w.distance }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, workouts=workouts)

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form['name'],
        'date': request.form['date'],
        'exercise': request.form['exercise'],
        'duration': request.form['duration'],
        'calories': request.form['calories'],
        'activity': request.form.get('activity', ''),
        'energy': request.form.get('energy', ''),
        'steps': request.form.get('steps', ''),
        'exercise_days': request.form.get('exercise_days', ''),
        'active_zone': request.form.get('active_zone', ''),
        'distance': request.form.get('distance', '')
    }
    workouts.append(data)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
