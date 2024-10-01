# Task 1: Setting Up the Flask Environment and Database Connection

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from password import my_password
import mysql.connector

app = Flask(__name__)
ma = Marshmallow(app)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = my_password
app.config['MYSQL_DB'] = 'gym_db'

# Establishing the connection
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = db.cursor()

# ----------------------------------------------------------------------------------------------------------------------
# Task 2: Implementing CRUD Operations for Members

# Add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    name = data['name']
    email = data['email']
    join_date = data['join_date']
    cursor.execute("INSERT INTO Members (name, email, join_date) VALUES (%s, %s, %s)", (name, email, join_date))
    db.commit()
    return jsonify({'message': 'Member added successfully'}), 201

# Retrieve a member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
    member = cursor.fetchone()
    if member:
        return jsonify({'id': member[0], 'name': member[1], 'email': member[2], 'join_date': member[3]})
    return jsonify({'message': 'Member not found'}), 404

# Update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    join_date = data['join_date']
    cursor.execute("UPDATE Members SET name = %s, email = %s, join_date = %s WHERE id = %s", (name, email, join_date, id))
    db.commit()
    return jsonify({'message': 'Member updated successfully'})

# Delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
    db.commit()
    return jsonify({'message': 'Member deleted successfully'})

# ----------------------------------------------------------------------------------------
# Task 3: Managing Workout Sessions

# Schedule a new workout session
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    member_id = data['member_id']
    session_date = data['session_date']
    duration = data['duration']
    cursor.execute("INSERT INTO WorkoutSessions (member_id, session_date, duration) VALUES (%s, %s, %s)", (member_id, session_date, duration))
    db.commit()
    return jsonify({'message': 'Workout session added successfully'}), 201

# Update a workout session by ID
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    data = request.get_json()
    session_date = data['session_date']
    duration = data['duration']
    cursor.execute("UPDATE WorkoutSessions SET session_date = %s, duration = %s WHERE id = %s", (session_date, duration, id))
    db.commit()
    return jsonify({'message': 'Workout session updated successfully'})

# View all workout sessions
@app.route('/workouts', methods=['GET'])
def get_workouts():
    cursor.execute("SELECT * FROM WorkoutSessions")
    workouts = cursor.fetchall()
    return jsonify(workouts)

# Retrieve all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
    workouts = cursor.fetchall()
    return jsonify(workouts)

if __name__ == '__main__':
    app.run(debug=True)
