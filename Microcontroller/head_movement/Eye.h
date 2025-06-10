#ifndef EYE_H
#define EYE_H

#include <Servo.h>
#include "Mosfet.h"

extern int currentAnglePositions[12];

class Eye {
    private:
      Servo servo_horizontal, servo_vertical, servo_lid;
      Mosfet* mosfet;
      int pinHorizontal, pinVertical, pinLid;
      char eyeId;

      int horizontalAngle;
      int verticalAngle;
      int lidAngle;

      static const int LR_ANGLE_MAX = 30;
      static const int UD_ANGLE_MAX = 40;

      static const int UP_SERVO_MAX = 130;
      static const int DOWN_SERVO_MIN = 50;
      static const int LEFT_SERVO_MAX = 60;
      static const int RIGHT_SERVO_MAX = 120;
      static const int LID_OPEN_MAX = 140;
      static const int LID_CLOSED_MIN = 40;

    public:
      Eye(Mosfet* mosfetPtr, int pinH, int pinV, int pinL, char eyeId);
      void init();
      void turn_on();
      void turn_off();
      bool is_on();
      void set_horizontal(int value);
      void set_vertical(int value);
      void set_lid(int percent);
      int get_lid_state();
      void look_at(int horizontal, int vertical);
};

#endif
