from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://mongodb:27017/')
db = client['doctors_db']
doctors_collection = db['doctors']

# Initial bootstrapping
initial_doctors = [
    {'id': "1001", 'firstName': "James", 'lastName': "Smith", 'speciality': "Cardiology"},
    {'id': "1002", 'firstName': "Linda", 'lastName': "Johnson", 'speciality': "Neurology"},
    {'id': "1003", 'firstName': "Robert", 'lastName': "Lee", 'speciality': "Orthopedics"},
    {'id': "1004", 'firstName': "Patricia", 'lastName': "Kim", 'speciality': "Pediatrics"},
    {'id': "1005", 'firstName': "Michael", 'lastName': "Brown", 'speciality': "Dermatology"},
    {'id': "1006", 'firstName': "Jennifer", 'lastName': "Davis", 'speciality': "General Surgery"},
    {'id': "1007", 'firstName': "William", 'lastName': "Garcia", 'speciality': "Psychiatry"},
    {'id': "1008", 'firstName': "Elizabeth", 'lastName': "Martinez", 'speciality': "Gynecology"}
]

# Insert initial values if the collection is empty
if doctors_collection.count_documents({}) == 0:
    doctors_collection.insert_many(initial_doctors)
    
@app.route('/hello')
def hello():
    greeting = "HELLO WORLD"
    return greeting

@app.route('/doctors', methods=["GET"])
def get_doctors():
    doctors_list = list(doctors_collection.find({}, {'_id': False}))
    return jsonify(doctors_list)

@app.route('/doctor/<doctor_id>', methods=["GET"])
def get_doctor(doctor_id):
    doctor = doctors_collection.find_one({'id': doctor_id}, {'_id': False})
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({'error': 'Doctor not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
