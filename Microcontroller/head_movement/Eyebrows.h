#ifndef EYEBROWS_H
#define EYEBROWS_H

#include <Servo.h>
#include "Mosfet.h"

extern int currentAnglePositions[12];

class EyeBrows {
    private:
      Servo servoLeft, servoRight;
      Mosfet *mosfetLeft, *mosfetRight;
      int pinLeft, pinRight;

      int angleLeft;
      int angleRight;

      static const int ROTATION_MAX = 30;
      static const int ANGLE_MAX = 120;
      static const int ANGLE_MIN = 60;

    public:
      EyeBrows(Mosfet* mosfetL, Mosfet* mosfetR, int pinL, int pinR);
      void init();
      void turn_on();
      void turn_off();
      bool is_out_of_limit(int angle);
      int get_mapped_value(int angle);
      void set_left(int value);
      void set_right(int value);
      void rotate(int left, int right);
};

#endif
