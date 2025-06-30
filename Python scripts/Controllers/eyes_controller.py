from math import degrees, atan2, sqrt
from numpy import matmul
from Controllers.config import MM_TO_PIXEL, EYE_LIMIT_HORIZONTAL, EYE_LIMIT_VERTICAL, DIFFERENCE_EYES, DIFFERENCE_HEAD

class EyesController:
    def __init__(self, controller):
        self.MM_TO_PIXEL = MM_TO_PIXEL
        self.LIMIT_HORIZONTAL = EYE_LIMIT_HORIZONTAL
        self.LIMIT_VERTICAL = EYE_LIMIT_VERTICAL

        self.raspberry = controller

        # In format (dx, dy) in mm
        self.DIFFERENCE_EYES = DIFFERENCE_EYES

        self.left_eye_diff = [[1, 0, 0, self.mm_to_pixel(self.DIFFERENCE_EYES[1])], 
                                [0, 1, 0, 0], 
                                [0, 0, 1, 0], 
                                [0, 0, 0, 1]]
        self.right_eye_diff = [[1, 0, 0, self.mm_to_pixel(self.DIFFERENCE_EYES[0])], 
                                 [0, 1, 0, 0], 
                                 [0, 0, 1, 0], 
                                 [0, 0, 0, 1]]
       
        # In format (dx, dy, dz) in mm
        self.DIFFERENCE_HEAD = DIFFERENCE_HEAD

        self.head_diff = [[1, 0, 0, self.mm_to_pixel(-self.DIFFERENCE_HEAD[0])], 
                           [0, 1, 0, self.mm_to_pixel(self.DIFFERENCE_HEAD[1])], 
                           [0, 0, 1, self.mm_to_pixel(-self.DIFFERENCE_HEAD[2])], 
                           [0, 0, 0, 1]]
        
        self.left_eye = 'L'
        self.right_eye = 'R'
        self.both_eyes = 'B'

        self.wake_up()

    def mm_to_pixel(self, mm):
        return mm * self.MM_TO_PIXEL

    def calculate_horizontal_degree(self, point):
        x, _, d, _ = point

        new_degree = degrees(atan2(x, d))

        new_degree = max(-self.LIMIT_HORIZONTAL, min(self.LIMIT_HORIZONTAL, new_degree))

        return int(new_degree)

    def calculate_vertical_degree(self, point):
        x, y, d, _ = point

        new_degree = degrees(atan2(y, sqrt(x**2 + d**2)))
        new_degree = max(-self.LIMIT_VERTICAL, min(self.LIMIT_VERTICAL, new_degree))

        return int(new_degree)

    def move_to_point(self, point):

        point[2] = self.mm_to_pixel(point[2])

        point = matmul(self.head_diff, point)

        point_to_left = matmul(self.left_eye_diff, point)

        config = (self.calculate_horizontal_degree(point_to_left), self.calculate_vertical_degree(point_to_left), self.raspberry.get_eye_lid_state(self.left_eye))

        self.raspberry.set_eye(self.left_eye, config)

        point_to_right = matmul(self.right_eye_diff, point)

        config = (self.calculate_horizontal_degree(point_to_right), self.calculate_vertical_degree(point_to_right), self.raspberry.get_eye_lid_state(self.right_eye))

        self.raspberry.set_eye(self.right_eye, config)
        
        self.raspberry.send_eye_move_command()

    def turn_on_eye(self):
        self.raspberry.send_turn_command("ON", "EYES")

    def turn_off_eye(self):
        self.raspberry.send_turn_command("OFF", "EYES")

    def wake_up(self):
        self.turn_on_eye()
        self.raspberry.set_eye(self.both_eyes, (0, 0, 85))
        self.raspberry.send_eye_move_command()
        self.turn_off_eye()
    
    def go_to_sleep(self):
        self.turn_on_eye()
        self.raspberry.set_eye(self.both_eyes, (0, 0, 0))
        self.raspberry.send_eye_move_command()
        self.turn_off_eye()



