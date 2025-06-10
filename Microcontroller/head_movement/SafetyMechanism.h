#ifndef SAFETYMECHANISM_H
#define SAFETYMECHANISM_H


#include <OneWire.h>
#include <DallasTemperature.h>
#include "Mosfet.h"


class SafetyMechanism {
    private:
        OneWire *onewire;
        DallasTemperature *temperatureSensors;
        Mosfet *leftEyeMosfet, *rightEyeMosfet, *mouthMosfet, *ventilators;

        int sensorPin;
        int externalBatteryPin;
        int buzzerPin;

        int currentPhase = 0;

        static const int TEMPERATURE_SENSORS_COUNT = 3;
        static constexpr float TEMPERATURE_PHASE_1_SWITCH = 45.0;
        static constexpr float TEMPERATURE_PHASE_2_SWITCH = 55.0;
        static constexpr float MINIMAL_ALLOWED_VOLTAGE = 6.5;

    public:
        SafetyMechanism(int sensorPin, int batteryPin, int buzzerPin, Mosfet *mosfets[4]);
        void init();
        int check_temperature();
        bool is_charged();
        bool is_in_danger();
        void execute_phase(int phase);
        void buzzer_alert(int count);
};

#endif
