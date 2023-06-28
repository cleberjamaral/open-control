import platform
#import RPi.GPIO as GPIO

class credential_controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.r1d0 = 17 # Wiegand D0 of reader 1
        self.r1d1 = 27 # Wiegand D1 of reader 1
        self.is_raspberry_pi = platform.machine().startswith('arm') or platform.machine().startswith('aarch') # Check if running on Raspberry Pi

        if self.is_raspberry_pi:
            self.view.display_message(f"Running on raspberry pi... Current platform: "+platform.machine())
            #import RPi.GPIO as GPIO
            #self.GPIO = GPIO
            
            import controller.wiegand as wiegand             
            import pigpio
            self.wiegand = wiegand
            self.pi = pigpio.pi()
        else:
            self.wiegand = None
            self.pi = None
            self.view.display_message(f"Peripherals won't work since it is not a Raspberry Pi! Current platform: "+platform.machine())
            
    def callback(self, bits, value):
        if bits == 34:
            w34 = (value >> 1) & 0xFFFFFFFF
            r = self.model.check_credential_exists(hex(w34)[2:])
            self.view.display_message(f"Result? {r}")

    def setup_gpio(self):
        if self.is_raspberry_pi:
            w = self.wiegand.decoder(self.pi, self.r1d0, self.r1d1, self.callback)
            self.view.display_message(f"GPIO configured on pins: "+str(self.r1d0)+" and "+str(self.r1d1))
            self.view.display_message(f"Waiting for credentials...")
        else:
            self.view.display_message(f"GPIO configuration skipped!")

    def cleanup(self):
        self.model.close_connection()
        self.view.display_message(f"Cleanup process executed!")

    def get_all_credentials(self):
        return self.model.get_all_credentials()

    def insert_credential(self, credential: str, registration_number: str, user_name: str):
        self.model.insert_credential(credential, registration_number, user_name)

    def check_credential_exists(self,credential):
        return self.model.check_credential_exists(credential)

    def delete_credential(self,credential):
        return self.model.delete_credential(credential)
