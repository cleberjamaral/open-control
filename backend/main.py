#!/usr/bin/env python

#pip install RPi.GPIO
#pip install flask flask-cors
#sudo apt-get install sqlite3
#sudo systemctl enable pigpiod
#sudo systemctl start pigpiod
#Edit open-control script to /etc/init.d/ make sure the path is correct

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from view.main_view import main_view
from model.credential_model import credential_model
from model.event_model import event_model
from controller.credential_controller import credential_controller
from controller.event_controller import event_controller
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def get_api():
    view.display_message(f"Open-control API is running!")
    return "Open-control API is running!"

@app.route('/api/credentials', methods=['GET'])
def get_credentials():
    credentials = controller.get_all_credentials()
    #view.display_message(f"Credential list: {credentials}, Reg.Number: {credentials}, User: {credentials}")
    return jsonify(credentials=credentials)

@app.route('/api/credentials', methods=['POST'])
def enroll_credential():
    credential = request.json['credential']
    registrationNumber = request.json['registrationNumber']
    userName = request.json['userName']
    view.display_message(f"Enrolling credential: {credential}, Reg.Number: {registrationNumber}, User: {userName}")
    controller.insert_credential(credential,registrationNumber,userName)
    return jsonify({"message":"Credential enrolled successfully"})

@app.route('/api/credentials/<string:credential>', methods=['PUT', 'OPTIONS'])
@cross_origin()
def update_credential(credential):
    if request.method == 'OPTIONS':
        # Handle the preflight OPTIONS request
        response = jsonify({'message': 'Preflight request received'})
        response.headers.add('Access-Control-Allow-Methods', 'PUT')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Handle the PUT request to update the credential
    credential = request.json['credential']
    registrationNumber = request.json['registrationNumber']
    userName = request.json['userName']
    view.display_message(f"Updating credential: {credential}, Reg.Number: {registrationNumber}, User: {userName}")
    controller.update_credential(credential, registrationNumber, userName)
    return jsonify({"message": "Credential updated successfully"})

@app.route('/api/credentials/<string:credential>', methods=['DELETE'])
def delete_credential(credential):
    view.display_message(f"Deleting credential: {credential}")
    
    if controller.delete_credential(credential):
        return jsonify({"message":"Credential deleted successfully"})
    else:
        return jsonify({"error":"Error on deleting credential="+credential}), 500


def connect(database_name):
    connection = sqlite3.connect(database_name, check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor

def create_tables(cursor,credential_table,event_table):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {credential_table} (credential TEXT, registration_number TEXT, user_name TEXT)")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {event_table} (date TEXT, credential TEXT, user_name TEXT, event_type TEXT)")

def close_connection(connection,cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

if __name__ == '__main__':
    DATABASE_NAME = "../open-control.db"
    CREDENTIAL_TABLE = "credential"
    EVENT_TABLE = "event"
    LOG_FILE = "open-control-backend.log"  # Specify the log file path here

    view = main_view(LOG_FILE)

    view.display_message(f"Starting open-control project... database file:{DATABASE_NAME}")
    CONNECTION, CURSOR = connect(DATABASE_NAME)
    create_tables(CURSOR,CREDENTIAL_TABLE,EVENT_TABLE)
    view.display_message(f"Connection with {DATABASE_NAME} established!")


    credential_model = credential_model(CONNECTION, CREDENTIAL_TABLE)
    event_model = event_model(CONNECTION, EVENT_TABLE)
    controller = credential_controller(credential_model, event_model, view)


    controller.setup_gpio()

    app.run(debug=True,host='0.0.0.0',port=5000,threaded=False,use_reloader=False)


