#ifndef MOUTH_H
#define MOUTH_H

#include <Servo.h>
#include "Mosfet.h"

extern int currentAnglePositions[12];

class Mouth {
    private:
      Servo servoUpperLeft, servoLowerLeft, servoUpperRight, servoLowerRight;
      Mosfet *mosfet;
      int pinUpperLeft, pinLowerLeft, pinUpperRight, pinLowerRight;

      int angleUpperLeft;
      int angleUpperRight;
      int angleLowerLeft;
      int angleLowerRight;

      static const int ROTATION_MAX = 30; 

      static const int ANGLE_MAX = 120;
      static const int ANGLE_MIN = 60; 

    public:
      Mouth(Mosfet* mosfetPtr, int pinUpperLeft, int pinLowerLeft, int pinUpperRight, int pinLowerRight);
      void init();
      void turn_on();
      void turn_off();
      bool is_out_of_limit(int angle);
      int get_mapped_value(int angle);
      void rotate(int upperLeft, int lowerLeft, int upperRight, int lowerRight);
};

#endif
