#ifndef MOSFET_H
#define MOSFET_H

#include <Arduino.h>

class Mosfet {
    private:
        int pin;
        bool state;
        static const int POWER_ON_DELAY = 100; 
        static const int POWER_OFF_DELAY = 400;

    public:
        Mosfet(int pin);
        void turn_on(int delayTime = POWER_ON_DELAY);
        void turn_off(int delayTime = POWER_ON_DELAY);
        bool is_on();
};

#endif
