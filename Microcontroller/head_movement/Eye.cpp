#include "Eye.h"

Eye::Eye(Mosfet* mosfetPtr, int pinH, int pinV, int pinL, char eyeId)
    : mosfet(mosfetPtr), pinHorizontal(pinH), pinVertical(pinV), pinLid(pinL), eyeId(eyeId),
      horizontalAngle(90), verticalAngle(90), lidAngle(90) { }

void Eye::init() {
    servo_horizontal.attach(pinHorizontal);
    servo_vertical.attach(pinVertical);
    servo_lid.attach(pinLid);

    turn_on();
    set_horizontal(0);
    set_vertical(0);
    set_lid(0);
    turn_off();
}

void Eye::turn_on() {
    mosfet->turn_on();
}

void Eye::turn_off() {
    mosfet->turn_off();
}

bool Eye::is_on() {
    return mosfet->is_on();
}

void Eye::set_horizontal(int value) {
    if (value < -LR_ANGLE_MAX || LR_ANGLE_MAX < value) return;
    horizontalAngle = int(map(value, -LR_ANGLE_MAX, LR_ANGLE_MAX, LEFT_SERVO_MAX, RIGHT_SERVO_MAX));
    servo_horizontal.write(horizontalAngle);
    currentAnglePositions[eyeId == 'L' ? 2 : 5] = value;
}

void Eye::set_vertical(int value) {
    if (value < -UD_ANGLE_MAX || UD_ANGLE_MAX < value) return;
    verticalAngle = int(map(value, -UD_ANGLE_MAX, UD_ANGLE_MAX, DOWN_SERVO_MIN, UP_SERVO_MAX));
    servo_vertical.write(verticalAngle);
    currentAnglePositions[eyeId == 'L' ? 3 : 6] = value;
}

void Eye::set_lid(int percent) {
    if (percent < 0 || 100 < percent) return;
    lidAngle = int(map(percent, 0, 100, LID_CLOSED_MIN, LID_OPEN_MAX));
    servo_lid.write(lidAngle);
    currentAnglePositions[eyeId == 'L' ? 4 : 7] = percent;
}

int Eye::get_lid_state() {
        return int(map(lidAngle, LID_CLOSED_MIN, LID_OPEN_MAX, 0, 100));
      }

void Eye::look_at(int horizontal, int vertical) {
    set_horizontal(horizontal);
    set_vertical(vertical);
}
