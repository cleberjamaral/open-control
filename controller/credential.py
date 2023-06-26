import platform
#import RPi.GPIO as GPIO

class credential_controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_raspberry_pi = platform.machine().startswith('arm') or platform.machine().startswith('aarch') # Check if running on Raspberry Pi

        if self.is_raspberry_pi:
            self.view.display_message(f"Running on raspberry pi... "+platform.machine())
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
        else:
            self.view.display_message(f"Not running on raspberry pi "+platform.machine()+", it won't work with access controller peripherals!")
            self.GPIO = None      

    def setup_gpio(self):
        if self.is_raspberry_pi:
            self.GPIO.setmode(self.GPIO.BCM)
            self.GPIO.setup(14, self.GPIO.IN)
            self.GPIO.setup(15, self.GPIO.IN)
            self.view.display_message(f"GPIO configured successfully!")
        else:
            self.view.display_message(f"GPIO configuration skipped!")

    def read_credential(self):
        try:
            self.view.display_message(f"Waiting for credentials...")
            while True and self.is_raspberry_pi:
                self.GPIO.wait_for_edge(14, self.GPIO.FALLING)
                card_number = ""
                for i in range(26):
                    GPIO.wait_for_edge(15, self.GPIO.RISING)
                    card_number += str(self.GPIO.input(15))
                self.model.insert_card_number(card_number)
                self.view.display_message(f"Card number {card_number} stored in the database.")
            self.view.display_message(f"Waiting for credentials loop finished!")

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        if self.is_raspberry_pi:
            self.GPIO.cleanup()
        self.model.close_connection()
        self.view.display_message(f"Cleanup process executed!")