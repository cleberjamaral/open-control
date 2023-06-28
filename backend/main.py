#pip install RPi.GPIO
#pip install flask flask-cors
#sudo apt-get install sqlite3
#sudo systemctl enable pigpiod
#sudo systemctl start pigpiod

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from model.credential import credential_model
from view.credential import credential_view
from controller.credential import credential_controller

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
    return jsonify(message="Credential enrolled successfully")

@app.route('/api/credentials/<string:credential>', methods=['DELETE'])
def delete_credential(credential):
    view.display_message(f"Deleting credential: {credential}")
    
    if controller.delete_credential(credential):
        return jsonify({"message":"Credential deleted successfully"})
    else:
        return jsonify({"error":"Error on deleting credential="+credential}), 500


if __name__ == '__main__':
    DATABASE_NAME = "../open-control.db"
    CREDENTIAL_TABLE = "credential"
    LOG_FILE = "open-control-backend.log"  # Specify the log file path here

    model = credential_model(DATABASE_NAME, CREDENTIAL_TABLE)
    view = credential_view(LOG_FILE)
    controller = credential_controller(model, view)

    view.display_message(f"Starting open-control project... database file:{DATABASE_NAME}")

    model.connect()
    view.display_message(f"Connection with {DATABASE_NAME} established!")

    controller.setup_gpio()

    app.run(debug=True,host='0.0.0.0')


