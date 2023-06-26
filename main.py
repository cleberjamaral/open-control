#pip install RPi.GPIO
#sudo apt-get install sqlite3

from model.credential import credential_model
from view.credential import credential_view
from controller.credential import credential_controller

if __name__ == '__main__':
    DATABASE_NAME = "open-control.db"
    CREDENTIAL_TABLE = "credential"

    model = credential_model(DATABASE_NAME, CREDENTIAL_TABLE)
    view = credential_view()
    controller = credential_controller(model, view)

    model.connect()
    controller.setup_gpio()
    controller.read_credential()