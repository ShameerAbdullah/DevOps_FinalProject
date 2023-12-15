from flask import Flask, jsonify, request
from pymongo import MongoClient, errors
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Using environment variables for database URI
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
try:
    client = MongoClient(mongo_uri)
    db = client['medical_center_db']
    medical_appointments_collection = db['medical_appointments']
except errors.ConnectionFailure:
    print("Could not connect to MongoDB")

initial_medical_appointments = [
    {'id': "1", 'patient': "John Doe", 'date': "21 Nov 2023", 'status': "Confirmed"},
    {'id': "2", 'patient': "Jane Smith", 'date': "22 Nov 2023", 'status': "Cancelled"},
    {'id': "3", 'patient': "Emily Johnson", 'date': "23 Nov 2023", 'status': "Pending"},
    {'id': "4", 'patient': "Michael Brown", 'date': "24 Nov 2023", 'status': "Confirmed"},
    {'id': "5", 'patient': "Linda Davis", 'date': "25 Nov 2023", 'status': "Rescheduled"},
    {'id': "6", 'patient': "Robert Wilson", 'date': "26 Nov 2023", 'status': "Confirmed"},
    {'id': "7", 'patient': "Maria Garcia", 'date': "27 Nov 2023", 'status': "No-show"},
    {'id': "8", 'patient': "James Miller", 'date': "28 Nov 2023", 'status': "Completed"},
    {'id': "9", 'patient': "Patricia Anderson", 'date': "29 Nov 2023", 'status': "Pending"},
    {'id': "10", 'patient': "Charles Thomas", 'date': "30 Nov 2023", 'status': "Cancelled"},
]

# Insert initial values if the collection is empty
if medical_appointments_collection.count_documents({}) == 0:
    medical_appointments_collection.insert_many(initial_medical_appointments)

@app.route('/hello')
def hello():
    return "Hello from Medical Center API!"

@app.route('/medical_appointments', methods=["GET"])
def get_medical_appointments():
    appointments_list = list(medical_appointments_collection.find({}, {'_id': False}))
    return jsonify(appointments_list)

@app.route('/medical_appointment/<appointment_id>', methods=["GET"])
def get_medical_appointment(appointment_id):
    appointment = medical_appointments_collection.find_one({'id': appointment_id}, {'_id': False})
    if appointment:
        return jsonify(appointment)
    else:
        return jsonify({'error': 'Appointment not found'}), 404

@app.route('/medical_appointment', methods=["POST"])
def create_medical_appointment():
    appointment_data = request.json
    medical_appointments_collection.insert_one(appointment_data)
    return jsonify({'message': 'Appointment created successfully'}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
