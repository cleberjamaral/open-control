import platform
#import RPi.GPIO as GPIO

class event_controller:
    def __init__(self, model):
        self.model = model

    def get_all_events(self):
        return self.model.get_all_events()
