#include "Eyebrows.h"

EyeBrows::EyeBrows(Mosfet* mosfetL, Mosfet* mosfetR, int pinL, int pinR) : mosfetLeft(mosfetL), mosfetRight(mosfetR), 
pinLeft(pinL), pinRight(pinR), angleLeft(90), angleRight(90) {}
      
void EyeBrows::init() {
  servoLeft.attach(pinLeft);
  servoRight.attach(pinRight); 
  
  turn_on();
  set_left(0);
  set_right(0);
  turn_off();
}

void EyeBrows::turn_on() {
  mosfetLeft->turn_on();
  mosfetRight->turn_on();
}

void EyeBrows::turn_off() {
  mosfetLeft->turn_off();
  mosfetRight->turn_off();
}

bool EyeBrows::is_out_of_limit(int angle) {
  return angle < -ROTATION_MAX || ROTATION_MAX< angle;
}

int EyeBrows::get_mapped_value(int angle) {
  return int(map(angle, -ROTATION_MAX, ROTATION_MAX, ANGLE_MIN, ANGLE_MAX));
}

void EyeBrows::set_left(int value) {
  if (is_out_of_limit(value)) return;

  currentAnglePositions[0] = value;

  angleLeft = get_mapped_value(value);
  servoLeft.write(angleLeft);
}

void EyeBrows::set_right(int value) {
  if (is_out_of_limit(value)) return;

  currentAnglePositions[1] = value;

  angleRight = get_mapped_value(value);
  servoRight.write(angleRight);
}

void EyeBrows::rotate(int left, int right) {        
  set_left(left);
  set_right(right);
}
