from Controllers.raspberry_controller import RaspberryController
from Controllers.eyes_controller import EyesController
import time

class FaceController:
    def __init__(self):
        self.microController = RaspberryController()
        self.eyesController = EyesController(self.microController)

        self.eyesController.wake_up()
        
    def look_at(self, point):
        self.eyesController.move_to_point(point)
    
    def get_emotions(self):
        time.sleep(0.1)
        return self.microController.get_emotions()
    
    def execute_emotion(self, emotion):
        self.microController.execute_emotion(emotion)

    def stop_emotion(self):
        self.microController.stop_emotion()

    def turn_part(self, state, part = "ALL"):
        ''' state = "ON" or "OFF"
            part = "EYES/EYEBROWS/MOUTH/VENTS/ALL"
        '''

        if state == "ON":
            self.microController.send_turn_command("ON", part)
        elif state == "OFF":
            self.microController.send_turn_command("OFF", part)

    def get_temperature(self):
        return self.microController.get_temperature()
    
    def get_battery_voltage(self):
        return self.microController.get_battery_voltage()

    def close_connection(self):
        self.turn_part("ON", "ALL")
        self.execute_emotion("NEUTRAL")
        time.sleep(1)
        self.eyesController.go_to_sleep()
        self.turn_part("OFF", "ALL")
        self.microController.close_connection()