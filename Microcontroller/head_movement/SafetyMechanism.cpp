#include "SafetyMechanism.h"

SafetyMechanism::SafetyMechanism(int sensorPin, int batteryPin, int buzzerPin, Mosfet *mosfets[4]) 
  : externalBatteryPin(batteryPin), buzzerPin(buzzerPin) {
    onewire = new OneWire(sensorPin);
    temperatureSensors = new DallasTemperature(onewire);

    leftEyeMosfet = mosfets[0];
    rightEyeMosfet = mosfets[1];
    mouthMosfet = mosfets[2];
    ventilators = mosfets[3];
  }

void SafetyMechanism::init() {
    temperatureSensors->begin();
    temperatureSensors->setResolution(9);
    pinMode(externalBatteryPin, INPUT);
    pinMode(buzzerPin, OUTPUT);
    }


int SafetyMechanism::check_temperature() {

    temperatureSensors->requestTemperatures();
    int newPhase = 0;

    for (int i = 0; i < TEMPERATURE_SENSORS_COUNT; i++) {
        float temperature = temperatureSensors->getTempCByIndex(i);
        
        if (TEMPERATURE_PHASE_2_SWITCH < temperature) {
            newPhase = max(newPhase, 2);
            buzzer_alert(3);
            break;

        } else if (TEMPERATURE_PHASE_1_SWITCH < temperature) {
            newPhase = max(newPhase, 1);
            buzzer_alert(2);

        } else {
            newPhase = max(newPhase, 0);
        }
    }

    if (currentPhase != newPhase) {
        execute_phase(newPhase);
        currentPhase = newPhase;
    }

    return currentPhase;
}

bool SafetyMechanism::is_charged() {
    int rawValue = analogRead(externalBatteryPin);
    float voltageOuter = rawValue * (3.3/1023.0);
    float voltageInner = voltageOuter * (83.0/27.0);

    if (voltageInner < MINIMAL_ALLOWED_VOLTAGE) {
        buzzer_alert(1);
        return false;      
    }

    return true;
}

bool SafetyMechanism::is_in_danger() {
    return check_temperature() == 2 || is_charged() == false;
}

void SafetyMechanism::execute_phase(int phase) {
    if (phase == 2) {
        leftEyeMosfet->turn_off();
        rightEyeMosfet->turn_off();
        mouthMosfet->turn_off();
        ventilators->turn_on();

    } else if (phase == 1) {
        ventilators->turn_on();

    } else {
        ventilators->turn_off();
    }
}

void SafetyMechanism::buzzer_alert(int count) {
    for (int i = 0; i < count; i++) {
        unsigned long start = millis();
        while (millis() - start < 250) {
            digitalWrite(buzzerPin, HIGH);
            delayMicroseconds(250);
            digitalWrite(buzzerPin, LOW);
            delayMicroseconds(250);
        }
        delay(250);
    }
    delay(2000);
}