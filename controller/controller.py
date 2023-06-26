import RPi.GPIO as GPIO

class CardController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.IN)
        GPIO.setup(15, GPIO.IN)

    def read_card_numbers(self):
        try:
            while True:
                GPIO.wait_for_edge(14, GPIO.FALLING)
                card_number = ""
                for i in range(26):
                    GPIO.wait_for_edge(15, GPIO.RISING)
                    card_number += str(GPIO.input(15))
                self.model.insert_card_number(card_number)
                self.view.display_message(f"Card number {card_number} stored in the database.")

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        GPIO.cleanup()
        self.model.close_connection()