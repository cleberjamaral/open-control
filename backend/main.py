#pip install RPi.GPIO
#pip install flask flask-cors
#sudo apt-get install sqlite3

from flask import Flask, request, jsonify
from flask_cors import CORS
from model.credential import credential_model
from view.credential import credential_view
from controller.credential import credential_controller

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for all routes

@app.route('/api/credentials', methods=['POST'])
def enroll_credential():
    credential = request.json['credential']
    view.display_message(f"Enrolling credential: {credential}")
    controller.insert_credential(credential,"","")
    return jsonify(message="Card enrolled successfully")

@app.route('/api/credentials', methods=['GET'])
def get_credentials():
    credentials = controller.get_all_credentials()
    view.display_message(f"Returning credential: {credentials}")
    return jsonify(credentials=credentials)

@app.route('/', methods=['GET'])
def get_api():
    view.display_message(f"Open-control API is running!")
    return "Open-control API is running!"

if __name__ == '__main__':
    DATABASE_NAME = "../open-control.db"
    CREDENTIAL_TABLE = "credential"
    LOG_FILE = "open-control-backend.log"  # Specify the log file path here

    model = credential_model(DATABASE_NAME, CREDENTIAL_TABLE)
    view = credential_view(LOG_FILE)
    controller = credential_controller(model, view)

    view.display_message(f"Starting open-control project... database file:{DATABASE_NAME}")

    model.connect()
    view.display_message(f"Connection with {DATABASE_NAME} stablished!")

    controller.setup_gpio()
    controller.read_credential()

    app.run(debug=True)


