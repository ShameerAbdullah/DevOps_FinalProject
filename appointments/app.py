from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['AppointmentSystemDB']
appointments_collection = db['Appointments']

initial_data = [
    {'id': "A1", 'doctor': "D1", 'date': "01 Jan 2024", 'rating': "Great"},
    {'id': "A2", 'doctor': "D2", 'date': "02 Jan 2024", 'rating': "Average"},
    {'id': "A3", 'doctor': "D3", 'date': "03 Jan 2024", 'rating': "Good"},
    {'id': "A4", 'doctor': "D1", 'date': "04 Jan 2024", 'rating': "Great"},
    {'id': "A5", 'doctor': "D4", 'date': "05 Jan 2024", 'rating': "Average"}
]

if appointments_collection.count_documents({}) == 0:
    appointments_collection.insert_many(initial_data)

@app.route('/welcome')
def welcome():
    greeting = "Welcome to the Appointment System!"
    return greeting

@app.route('/appointments', methods=["GET"])
def list_appointments():
    appointments_list = list(appointments_collection.find({}, {'_id': False}))
    return jsonify(appointments_list)

@app.route('/appointment/<appointment_id>', methods=["GET"])
def get_specific_appointment(appointment_id):
    appointment = appointments_collection.find_one({'id': appointment_id}, {'_id': False})
    if appointment:
        return jsonify(appointment)
    else:
        return jsonify({'error': 'Appointment not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
