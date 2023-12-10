from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['healthcare_db']
doctors_collection = db['healthcare_professionals']

initial_data = [
    {'id': "D1", 'firstName': "John", 'lastName': "Smith", 'speciality': "Pediatrics"},
    {'id': "D2", 'firstName': "Jane", 'lastName': "Doe", 'speciality': "Orthopedics"},
    {'id': "D3", 'firstName': "Emily", 'lastName': "Johnson", 'speciality': "Oncology"},
    {'id': "D4", 'firstName': "Michael", 'lastName': "Brown", 'speciality': "Neurology"},
    {'id': "D5", 'firstName': "Sophia", 'lastName': "Wilson", 'speciality': "Dentistry"}
]

if doctors_collection.count_documents({}) == 0:
    doctors_collection.insert_many(initial_data)

@app.route('/welcome')
def welcome():
    greeting = "Welcome to the Healthcare System!"
    return greeting

@app.route('/professionals', methods=["GET"])
def list_professionals():
    professionals_list = list(doctors_collection.find({}, {'_id': False}))
    return jsonify(professionals_list)

@app.route('/professional/<professional_id>', methods=["GET"])
def get_specific_professional(professional_id):
    professional = doctors_collection.find_one({'id': professional_id}, {'_id': False})
    if professional:
        return jsonify(professional)
    else:
        return jsonify({'error': 'Professional not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
