from Controllers.raspberry_controller import RaspberryController
from Controllers.eyes_controller import EyesController

class FaceController:
    def __init__(self):
        self.microController = RaspberryController()
        self.eyesController = EyesController(self.microController)

        self.eyesController.wake_up()
        
    def look_at(self, point):
        self.eyesController.move_to_point(point)
    
    def get_emotions(self):
        return self.microController.get_emotions()
    
    def execute_emotion(self, emotion):
        self.microController.execute_emotion(emotion)

    def turn_part(self, state, part = "ALL"):
        ''' state = "ON" or "OFF"
            part = "EYES/EYEBROWS/MOUTH/VENTS/ALL"
        '''

        if state == "ON":
            self.microController.send_turn_command("ON", part)
        elif state == "OFF":
            self.microController.send_turn_command("OFF", part)
    
    def close_connection(self):
        self.turn_part("ON", "ALL")
        self.eyesController.go_to_sleep()
        self.turn_part("OFF", "ALL")
        self.microController.close_connection()

        


    

