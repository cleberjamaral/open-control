#pip install RPi.GPIO
#sudo apt-get install sqlite3

from model.credential import credential_model
from view.credential import credential_view
from controller.credential import credential_controller

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
