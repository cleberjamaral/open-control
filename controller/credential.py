import platform
#import RPi.GPIO as GPIO

class credential_controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_raspberry_pi = platform.machine() == 'armv7l'  # Check if running on Raspberry Pi

        if self.is_raspberry_pi:
            self.view.display_message(f"Running on raspberry pi...")
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
        else:
            self.view.display_message(f"Not running on raspberry pi, it won't work with access controller peripherals!")
            self.GPIO = None      

    def setup_gpio(self):
        if self.is_raspberry_pi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(14, GPIO.IN)
            GPIO.setup(15, GPIO.IN)

    def read_credential(self):
        try:
            while True and self.is_raspberry_pi:
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
        if self.is_raspberry_pi:
            GPIO.cleanup()
        self.model.close_connection()