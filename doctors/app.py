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
    db = client['healthcare_db']
    doctors_collection = db['healthcare_professionals']
except errors.ConnectionFailure:
    print("Could not connect to MongoDB")

initial_healthcare_professionals = [
    {'id': "1", 'firstName': "John", 'lastName': "Doe", 'speciality': "Cardiology"},
    {'id': "2", 'firstName': "Jane", 'lastName': "Smith", 'speciality': "Neurology"},
    {'id': "3", 'firstName': "Emily", 'lastName': "Johnson", 'speciality': "Dermatology"},
    {'id': "4", 'firstName': "Michael", 'lastName': "Brown", 'speciality': "Pediatrics"},
    {'id': "5", 'firstName': "Linda", 'lastName': "Davis", 'speciality': "General Practice"},
    {'id': "6", 'firstName': "Robert", 'lastName': "Wilson", 'speciality': "Orthopedics"},
    {'id': "7", 'firstName': "Maria", 'lastName': "Garcia", 'speciality': "Gynecology"},
    {'id': "8", 'firstName': "James", 'lastName': "Miller", 'speciality': "Oncology"},
    {'id': "9", 'firstName': "Patricia", 'lastName': "Anderson", 'speciality': "Psychiatry"},
    {'id': "10", 'firstName': "Charles", 'lastName': "Thomas", 'speciality': "Anesthesiology"},
    {'id': "11", 'firstName': "Lisa", 'lastName': "White", 'speciality': "Rheumatology"},
    {'id': "12", 'firstName': "Paul", 'lastName': "Harris", 'speciality': "Ophthalmology"},
    {'id': "13", 'firstName': "Nancy", 'lastName': "Clark", 'speciality': "Endocrinology"},
    {'id': "14", 'firstName': "Kevin", 'lastName': "Lewis", 'speciality': "Urology"},
    {'id': "15", 'firstName': "Susan", 'lastName': "Lee", 'speciality': "Gastroenterology"},
]


# Insert initial values if the collection is empty
if doctors_collection.count_documents({}) == 0:
    doctors_collection.insert_many(initial_healthcare_professionals)

@app.route('/hello')
def hello():
    return "Hello from Healthcare Professionals API!"

@app.route('/healthcare_professionals', methods=["GET"])
def get_healthcare_professionals():
    professionals_list = list(doctors_collection.find({}, {'_id': False}))
    return jsonify(professionals_list)

@app.route('/healthcare_professional/<professional_id>', methods=["GET"])
def get_healthcare_professional(professional_id):
    professional = doctors_collection.find_one({'id': professional_id}, {'_id': False})
    if professional:
        return jsonify(professional)
    else:
        return jsonify({'error': 'Healthcare professional not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
