#include <Arduino.h>
#include "Emotions.h"

EmotionEntry Emotions::emotionMap[EMOTIONS_COUNT];
int Emotions::emotionCount = 0;

void Emotions::initialize() {
    emotionMap[emotionCount].name = "SMILE";
    emotionMap[emotionCount].data = smile;
    emotionMap[emotionCount++].steps = 7;

    emotionMap[emotionCount].name = "ANGER";
    emotionMap[emotionCount].data = anger;
    emotionMap[emotionCount++].steps = 7;


    emotionMap[emotionCount].name = "SURPRISE";
    emotionMap[emotionCount].data = surprise;
    emotionMap[emotionCount++].steps = 7;

}

int (*Emotions::get_emotion(const String& name))[13] {
    for (int i = 0; i < emotionCount; i++) {
        if (emotionMap[i].name == name) {
            return emotionMap[i].data;
        }
    }
    return nullptr;
}

int Emotions::get_steps(const String& name) {
    for (int i = 0; i < emotionCount; i++) {
        if (emotionMap[i].name == name) {
            return emotionMap[i].steps;
        }
    }
    return 0;
}

// time, eyebrowL, eyebrowR, eyeL_horizontal, eyeL_vertical, eyeL_lid, eyeR_horizontal, eyeR_vertical, eyeR_lid, mouth_upperLeft, mouth_lowerLeft, mouth_upperRight, mouth_lowerRight

int smile[][13] = {
    {100,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
    {400, 10, -10,      0, 0, 85, 0, 0, 85,     10, 10, -10, -10},
    {300, 20, -20,      0, 0, 85, 0, 0, 85,     20, 20, -20, -20},
    {200, 30, -30,      0, 0, 85, 0, 0, 85,     30, 30, -30, -30},
    {1500, 20, -20,      0, 0, 85, 0, 0, 85,     20, 20, -20, -20},
    {500, 10, -10,      0, 0, 85, 0, 0, 85,     10, 10, -10, -10},
    {500,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
};

int anger[][13] = {
    {100,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
    {400, -10, 10,      0, 0, 85, 0, 0, 85,     -10, -10, 10, 10},
    {300, -20, 20,      0, 0, 85, 0, 0, 85,     -20, -20, 20, 20},
    {200, -30, 30,      0, 0, 85, 0, 0, 85,     -30, -30, 30, 30},
    {1500, -20, 20,      0, 0, 85, 0, 0, 85,     -20, -20, 20, 20},
    {500, -10, 10,      0, 0, 85, 0, 0, 85,     -10, -10, 10, 10},
    {500,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
};

int surprise[][13] = {
    {100,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
    {400, 10, -10,      0, 0, 85, 0, 0, 85,     -10, 10, 10, -10},
    {300, 20, -20,      0, 0, 85, 0, 0, 85,     -20, 20, 20, -20},
    {200, 30, -30,      0, 0, 85, 0, 0, 85,     -30, 30, 30, -30},
    {1500, 20, -20,      0, 0, 85, 0, 0, 85,     -20, 20, 20, -20},
    {500, 10, -10,      0, 0, 85, 0, 0, 85,     -10, 10, 10, -10},
    {500,   0,  0,      0, 0, 85, 0, 0, 85,       0,   0,  0,  0},
};