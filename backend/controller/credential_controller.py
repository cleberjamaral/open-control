import platform
#import RPi.GPIO as GPIO

class credential_controller:
    def __init__(self, credential_model, event_model, view):
        self.credential_model = credential_model
        self.event_model = event_model
        self.view = view
        self.r1d0 = 17 # Wiegand D0 of reader 1
        self.r1d1 = 27 # Wiegand D1 of reader 1
        self.gate_in = 23 # Open the gate for entrance
        self.mili = 1000 # 1 ms = 1000 us
        self.is_raspberry_pi = platform.machine().startswith('arm') or platform.machine().startswith('aarch') # Check if running on Raspberry Pi

        if self.is_raspberry_pi:
            self.view.display_message(f"Running on raspberry pi... Current platform: "+platform.machine())
            #import RPi.GPIO as GPIO
            #self.GPIO = GPIO
            
            import controller.wiegand as wiegand             
            import pigpio
            self.wiegand = wiegand
            self.pigpio = pigpio
            self.set_gate_pins()
            self.open_gate_in()
            self.pigpio.pi().write(self.gate_in, 0)
        else:
            self.wiegand = None
            self.pigpio = None
            self.view.display_message(f"Peripherals won't work since it is not a Raspberry Pi! Current platform: "+platform.machine())

    def set_gate_pins(self):
        self.pigpio.pi().set_mode(self.gate_in, self.pigpio.OUTPUT)

    def open_gate_in(self):
        #self.pigpio.pulse(1 << self.gate_in, 0, 2000 * self.mili)
        self.pigpio.pi().write(self.gate_in, 1)
        import time
        time.sleep(1)
        self.pigpio.pi().write(self.gate_in, 0)

    def callback(self, bits, value):
        if bits == 34:
            w34 = (value >> 1) & 0xFFFFFFFF
            credentials = self.credential_model.check_credential_exists(hex(w34)[2:])
            if credentials:
                self.view.display_message(f"Access granted for credential {hex(w34)[2:]}!")
                for credential in credentials:
                    self.event_model.insert_event(credential[0], credential[2], "Access granted!")
                self.open_gate_in()
            else:
                self.view.display_message(f"Credential {hex(w34)[2:]} not found, access denied!")
                self.event_model.insert_event(hex(w34)[2:], "User not enrolled", "Access denied!")

    def setup_gpio(self):
        if self.is_raspberry_pi:
            w = self.wiegand.decoder(self.pigpio.pi(), self.r1d0, self.r1d1, self.callback)
            self.view.display_message(f"GPIO configured on pins: "+str(self.r1d0)+" and "+str(self.r1d1))
            self.view.display_message(f"Waiting for credentials...")
        else:
            self.view.display_message(f"GPIO configuration skipped!")

    def cleanup(self):
        self.credential_model.close_connection()
        self.view.display_message(f"Cleanup process executed!")

    def get_all_credentials(self):
        return self.credential_model.get_all_credentials()

    def insert_credential(self, credential: str, registration_number: str, user_name: str):
        self.credential_model.insert_credential(credential, registration_number, user_name)

    def update_credential(self, credential: str, registration_number: str, user_name: str):
        self.credential_model.update_credential(credential, registration_number, user_name)

    def check_credential_exists(self,credential):
        return self.credential_model.check_credential_exists(credential)

    def delete_credential(self,credential):
        return self.credential_model.delete_credential(credential)

    def insert_event(self, date: str, credential: str, user_name: str, event_type: str):
        self.event_model.insert_event(date, credential, user_name, event_type)
