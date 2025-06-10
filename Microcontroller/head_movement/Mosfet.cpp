#include "Mosfet.h"

Mosfet::Mosfet(int pin) : pin(pin), state(false) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
}

void Mosfet::turn_on(int delayTime) {
    digitalWrite(pin, HIGH);
    state = true;
    delay(delayTime);
}

void Mosfet::turn_off(int delayTime) {
    delay(delayTime);
    digitalWrite(pin, LOW);
    state = false;
}

bool Mosfet::is_on() {
    return state;
}