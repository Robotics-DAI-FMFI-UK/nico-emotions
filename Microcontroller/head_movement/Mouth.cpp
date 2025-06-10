#include "Mouth.h"

Mouth::Mouth(Mosfet* mosfet, int pinUpperLeft, int pinLowerLeft, int pinUpperRight, int pinLowerRight) 
  : mosfet(mosfet), pinUpperLeft(pinUpperLeft), pinLowerLeft(pinLowerLeft), pinUpperRight(pinUpperRight), pinLowerRight(pinLowerRight),
  angleUpperLeft(90), angleUpperRight(90), angleLowerLeft(90), angleLowerRight(90) {}

void Mouth::init() {
  servoUpperLeft.attach(pinUpperLeft);
  servoUpperRight.attach(pinUpperRight);
  servoLowerLeft.attach(pinLowerLeft);
  servoLowerRight.attach(pinLowerRight);

  turn_on();
  rotate(0, 0, 0, 0);
  turn_off();
}

void Mouth::turn_on() {
  mosfet->turn_on();
}

void Mouth::turn_off() {
  mosfet->turn_off();
}

bool Mouth::is_out_of_limit(int angle) {
  return angle < -ROTATION_MAX || ROTATION_MAX< angle;
}

int Mouth::get_mapped_value(int angle) {
  return int(map(angle, -ROTATION_MAX, ROTATION_MAX, ANGLE_MIN, ANGLE_MAX));
}

void Mouth::rotate(int upperLeft, int lowerLeft, int upperRight, int lowerRight) {        
  if (is_out_of_limit(upperLeft) || is_out_of_limit(upperRight) || 
      is_out_of_limit(lowerLeft) || is_out_of_limit(lowerRight)) {
    return;
  }

  currentAnglePositions[8] = upperLeft;
  currentAnglePositions[9] = lowerLeft;
  currentAnglePositions[10] = upperRight;
  currentAnglePositions[11] = lowerRight;

  angleUpperLeft = get_mapped_value(upperLeft);
  angleUpperRight = get_mapped_value(upperRight);
  angleLowerLeft = get_mapped_value(lowerLeft);
  angleLowerRight = get_mapped_value(lowerRight);

  servoUpperLeft.write(angleUpperLeft);
  servoUpperRight.write(angleUpperRight);
  servoLowerLeft.write(angleLowerLeft);
  servoLowerRight.write(angleLowerRight);
}
