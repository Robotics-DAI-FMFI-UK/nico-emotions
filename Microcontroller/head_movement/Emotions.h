#ifndef EMOTIONS_H
#define EMOTIONS_H

#include <Arduino.h>

#define EMOTIONS_COUNT 3

extern int smile[][13];
extern int anger[][13];
extern int surprise[][13];

struct EmotionEntry {
    String name;
    int (*data)[13];
    int steps;
};

class Emotions {
private:
    static EmotionEntry emotionMap[EMOTIONS_COUNT];
    static int emotionCount;

public:
    static void initialize();
    static int (*get_emotion(const String& name))[13];
    static int get_steps(const String& name);
};

#endif