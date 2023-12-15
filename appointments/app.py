from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://mongodb-service:27017/')
db = client['appointments_db']
appointments_collection = db['appointments']

# Initial bootstrapping
initial_appointments = [
    {'id': "101", 'doctor': "Dr. Smith", 'date': "2024-01-15", 'rating': "Excellent", 'patient': "John Doe"},
    {'id': "102", 'doctor': "Dr. Johnson", 'date': "2024-01-16", 'rating': "Good", 'patient': "Emily Davis"},
    {'id': "103", 'doctor': "Dr. Clark", 'date': "2024-01-17", 'rating': "Fair", 'patient': "Michael Brown"},
    {'id': "104", 'doctor': "Dr. Wilson", 'date': "2024-01-18", 'rating': "Bad", 'patient': "Linda Taylor"},
    {'id': "105", 'doctor': "Dr. Martinez", 'date': "2024-01-19", 'rating': "Good", 'patient': "Robert Moore"},
    {'id': "106", 'doctor': "Dr. Garcia", 'date': "2024-01-20", 'rating': "Excellent", 'patient': "Barbara Young"},
    {'id': "107", 'doctor': "Dr. Brown", 'date': "2024-01-21", 'rating': "Fair", 'patient': "James Hall"},
    {'id': "108", 'doctor': "Dr. Miller", 'date': "2024-01-22", 'rating': "Poor", 'patient': "Patricia King"},
]

# Insert initial values if the collection is empty
if appointments_collection.count_documents({}) == 0:
    appointments_collection.insert_many(initial_appointments)

@app.route('/hello')
def hello():
    greeting = "HELLO WORLD"
    return greeting

@app.route('/appointments', methods=["GET"])
def get_appointments():
    appointments_list = list(appointments_collection.find({}, {'_id': False}))
    return jsonify(appointments_list)

@app.route('/appointment/<appointment_id>', methods=["GET"])
def get_appointment(appointment_id):
    appointment = appointments_collection.find_one({'id': appointment_id}, {'_id': False})
    if appointment:
        return jsonify(appointment)
    else:
        return jsonify({'error': 'Appointment not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
