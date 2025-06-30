import serial
import time

from Controllers.find_microcontroller import find_microcontroller
from Controllers.config import EYE_LIMIT_HORIZONTAL, EYE_LIMIT_VERTICAL, EYE_LIMIT_LID

class RaspberryController:
    def __init__(self):

        baudrate=115200

        self.left_eye_state = (0, 0, 0)
        self.right_eye_state = (0, 0, 0)

        self.EYE_LIMIT_HORIZONTAL = EYE_LIMIT_HORIZONTAL
        self.EYE_LIMIT_VERTICAL = EYE_LIMIT_VERTICAL
        self.EYE_LIMIT_LID = EYE_LIMIT_LID

        self.left_eye = 'L'
        self.right_eye = 'R'
        self.both_eyes = 'B'
        
        port = find_microcontroller()
        if port is None:
            print("Microcontroller not found")
            exit(1)
        
        try:
            self.ser = serial.Serial(port, baudrate)
            time.sleep(2)
        except serial.SerialException as e:
            print(f"Error opening serial port {port}: {e}")
            raise
    
    def send_command(self, command):
        self.ser.write((command + '\n').encode())

    def send_eye_move_command(self):
        lh, lv, ll = self.left_eye_state
        rh, rv, rl = self.right_eye_state
        self.send_command(f"EYES:{lh},{lv},{ll}/{rh},{rv},{rl}")

    def send_turn_command(self, type, part):
        self.send_command(f"TURN_{type}:{part}")

    def set_eye(self, eye, config = (0, 0, 0)):
        if eye == self.both_eyes:
            self.left_eye_state = config
            self.right_eye_state = config
        elif eye == self.left_eye:
            self.left_eye_state = config
        elif eye == self.right_eye:
            self.right_eye_state = config
        
    def get_eye_lid_state(self, eye):
        if eye == self.left_eye:
            return self.left_eye_state[2]
        elif eye == self.right_eye:
            return self.right_eye_state[2]
        
    def get_emotions(self):
        self.send_command("GET:EMOTIONS")
        time.sleep(0.1)
        start_time = time.time()
        timeout = 2

        while True:
            if self.ser.in_waiting == 0 and (time.time() - start_time) > timeout:
                return []
            
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode('utf-8').strip()
                
                if response.startswith("EMOTIONS: "):
                    emotions_str = response[len("EMOTIONS: "):]
                    return [e.strip() for e in emotions_str.split(',') if e.strip()] 
    
    def execute_emotion(self, emotion):
        emotions = self.get_emotions()
        if emotion in emotions:
            self.send_command(f"EMOTION:{emotion}")
        else:
            print(f"Emotion '{emotion}' not recognized.")

    def stop_emotion(self):
        self.send_command("STOP_EMOTION")

    def get_temperature(self):
        self.send_command("GET:TEMPERATURES")
        time.sleep(0.1)
        response = self.ser.readline().decode('utf-8').strip()
        return float(response)
    
    def get_battery_voltage(self):
        self.send_command("GET:BATTERY_VOLTAGE")
        time.sleep(0.1)
        response = self.ser.readline().decode('utf-8').strip()
        return float(response)

    def close_connection(self):
        self.ser.close()

