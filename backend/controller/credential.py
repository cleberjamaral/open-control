import platform
#import RPi.GPIO as GPIO

class credential_controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.is_raspberry_pi = platform.machine().startswith('arm') or platform.machine().startswith('aarch') # Check if running on Raspberry Pi

        if self.is_raspberry_pi:
            self.view.display_message(f"Running on raspberry pi... Current platform:"+platform.machine())
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
        else:
            self.view.display_message(f"Peripherals won't work since it is not a Raspberry Pi! Current platform:"+platform.machine())
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
            self.view.display_message(f"Credentials loop finished!")

        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        if self.is_raspberry_pi:
            self.GPIO.cleanup()
        self.model.close_connection()
        self.view.display_message(f"Cleanup process executed!")

    def insert_credential(self, credential: str, registration_number: str, user_name: str):
        self.model.insert_credential(credential, registration_number, user_name)

    def get_all_credentials(self):
        return self.model.get_all_credentials()