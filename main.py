#pip install RPi.GPIO
#sudo apt-get install sqlite3

from model.model import CardModel
from view.view import CardView
from controller.controller import CardController

if __name__ == '__main__':
    DATABASE_NAME = "cards.db"
    TABLE_NAME = "cards"

    model = CardModel(DATABASE_NAME, TABLE_NAME)
    view = CardView()
    controller = CardController(model, view)

    model.connect()
    controller.setup_gpio()
    controller.read_card_numbers()