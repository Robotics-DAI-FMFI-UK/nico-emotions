#include "head_movement.h"

Mosfet leftEyeMosfet(7);
Mosfet rightEyeMosfet(6);
Mosfet mouthMosfet(18);
Mosfet ventilators(17);
Mosfet* mosfetArray[] = {&leftEyeMosfet, &rightEyeMosfet, &mouthMosfet, &ventilators};

SafetyMechanism safetyMechanism(14, A0, 16, mosfetArray);
Eye rightEye(&rightEyeMosfet, 3, 4, 5, 'R');
Eye leftEye(&leftEyeMosfet, 19, 20, 21, 'L');
EyeBrows eyebrows(&leftEyeMosfet, &rightEyeMosfet, 22, 2);
Mouth mouth(&mouthMosfet, 10, 11, 12, 13);

bool isEmotionActive = false;
String activeEmotion = "";
int emotionStep = 0;
bool systemInDanger = false;

int currentAnglePositions[12] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void setup() {
  Serial.begin(115200);  
  Emotions::initialize();
  safetyMechanism.init();

  command_turn_on("ALL");
  leftEye.init();
  rightEye.init();
  eyebrows.init();
  mouth.init();
  command_turn_off("ALL");
}

void extract_eye_parameters(const char* input, int* parameters) {
  sscanf(input, "%d,%d,%d/%d,%d,%d", 
         &parameters[0], &parameters[1], &parameters[2], 
         &parameters[3], &parameters[4], &parameters[5]);
}

void command_eyes(String input) {
  // input in format h,v,l/h,v,l

  int parameters[6];
  extract_eye_parameters(input.c_str(), parameters);

  int leftH = parameters[0];
  int leftV = parameters[1];
  int leftL = parameters[2];
  int rightH = parameters[3];
  int rightV = parameters[4];
  int rightL = parameters[5];

  leftEye.look_at(leftH, leftV);
  rightEye.look_at(rightH, rightV);

  leftEye.set_lid(leftL);
  rightEye.set_lid(rightL);
}

void extract_eyebrow_parameters(const char* input, int* parameters) {
  sscanf(input, "%d/%d", &parameters[0], &parameters[1]);
}

void command_eyebrows(String input) {
  // in format L/R

  int parameters[2];
  extract_eyebrow_parameters(input.c_str(), parameters);
  int left = parameters[0];
  int right = parameters[1]; 

  eyebrows.rotate(left, right);
}

void extract_mouth_parameters(const char* input, int* parameters) {
  sscanf(input, "%d,%d/%d,%d", &parameters[0], &parameters[1], &parameters[2], &parameters[3]);
}

void command_mouth(String input) {
  // in format UL,LL/UR,LR
  // UL - upper left, LL - lower left, UR - upper right, LR - lower right

  int parameters[4];
  extract_mouth_parameters(input.c_str(), parameters);
  int upperLeft = parameters[0];
  int lowerLeft = parameters[1];
  int upperRight = parameters[2]; 
  int lowerRight = parameters[3];

  mouth.rotate(upperLeft, lowerLeft, upperRight, lowerRight);
}

void command_face(String input) {
  // in format eyebrowL/eyebrowR:eyeL_horizontal,eyeL_vertical,eyeL_lid/eyeR_horizontal,eyeR_vertical,eyeR_lid:mouth_upperLeft,mouth_lowerLeft/mouth_upperRight,mouth_lowerRight

  int split1 = input.indexOf(':');
  int split2 = input.indexOf(':', split1 + 1);

  String eyebrowsInput = input.substring(0, split1);
  String eyesInput = input.substring(split1 + 1, split2);
  String mouthInput = input.substring(split2 + 1);

  command_eyebrows(eyebrowsInput);
  command_eyes(eyesInput);
  command_mouth(mouthInput);
}

void command_turn_on(String target) {
  if (target == "EYES") {
    leftEye.turn_on();
    rightEye.turn_on();

  } else if (target == "EYEBROWS") {
    eyebrows.turn_on();

  } else if (target == "MOUTH") {
    mouth.turn_on();

  } else if (target == "ALL") {
    leftEye.turn_on();
    rightEye.turn_on();
    eyebrows.turn_on();
    mouth.turn_on();

  } else if (target == "VENTS") {
    ventilators.turn_on();

  } else {
    Serial.println("Invalid TURN_ON target!");
  }
}

void command_turn_off(String target) {
  if (target == "EYES") {
    leftEye.turn_off();
    rightEye.turn_off();

  } else if (target == "EYEBROWS") {
    eyebrows.turn_off();

  } else if (target == "MOUTH") {
    mouth.turn_off();

  } else if (target == "ALL") {
    leftEye.turn_off();
    rightEye.turn_off();
    eyebrows.turn_off();
    mouth.turn_off();

  } else if (target == "VENTS") {
    ventilators.turn_off();

  } else {
    Serial.println("Invalid TURN_OFF target!");
  }
}

void start_emotion(String emotion) {
  isEmotionActive = true;
  activeEmotion = emotion;
  execute_emotion(emotion);
}

void execute_emotion(String emotion) {

  int (*emotionArray)[13] = Emotions::get_emotion(emotion);
  if (emotionArray == nullptr) {
    Serial.println("Emotion not found!");
    return;
  }

  int steps = Emotions::get_steps(emotion);

  if (steps <= emotionStep) {
    stop_emotion();
    return;
  }

  int* currentEmotion = emotionArray[emotionStep];
  double currentSteps[12] = {};

  for (int i = 0; i < 12; i++) {
    currentSteps[i] = currentAnglePositions[i];
  }

  double angleSteps[12] = {};

  for (int i = 0; i < 12; i++) {
    angleSteps[i] = (currentEmotion[i+1] - currentAnglePositions[i]) / 50.0;
  }
  
  int timeDelay = currentEmotion[0];
  float tStep = (timeDelay / 50.0)*1000;

  for (int t = 0; t < 50; t++) {
    eyebrows.rotate(int(currentSteps[0]+0.5), int(currentSteps[1]+0.5));
    leftEye.look_at(int(currentSteps[2]+0.5), int(currentSteps[3]+0.5));
    leftEye.set_lid(int(currentSteps[4]+0.5));
    rightEye.look_at(int(currentSteps[5]+0.5), int(currentSteps[6]+0.5));
    rightEye.set_lid(int(currentSteps[7]+0.5));
    mouth.rotate(int(currentSteps[8]+0.5), int(currentSteps[9]+0.5), int(currentSteps[10]+0.5), int(currentSteps[11]+0.5));

    for (int i = 0; i < 12; i++) {
      currentSteps[i] += angleSteps[i];
    }
    delayMicroseconds(uint32_t(tStep + 0.5));
  }
  emotionStep++;
}

void stop_emotion() {
  isEmotionActive = false;
  activeEmotion = "";
  emotionStep = 0;
}

void blink_randomly() {
  int leftLidBefore = leftEye.get_lid_state();
  int rightLidBefore = rightEye.get_lid_state();

  if (leftLidBefore <= 10 && rightLidBefore <= 10) return;

  bool leftEyeWasOff = !leftEye.is_on();
  bool rightEyeWasOff = !rightEye.is_on();

  if (leftEyeWasOff) {
    leftEye.turn_on();
  }

  if (rightEyeWasOff) {
    rightEye.turn_on();
  }

  leftEye.set_lid(0); 
  rightEye.set_lid(0);

  delay(random(80, 140));

  leftEye.set_lid(leftLidBefore); 
  rightEye.set_lid(rightLidBefore);
  
  if (leftEyeWasOff) {
    leftEye.turn_off();
  }
  
  if (rightEyeWasOff) {
    rightEye.turn_off();
  }
}

void loop() {
  static unsigned long lastSafetyCheck = 0;
  static const unsigned long safetyCheckInterval = 30000;

  if (millis() - lastSafetyCheck >= safetyCheckInterval) {
    lastSafetyCheck = millis();
    if (safetyMechanism.is_in_danger()) {
      systemInDanger = true;
    } else {
      systemInDanger = false;
    }
  }

  if (systemInDanger) {
    return;
  }

  static unsigned long lastBlink = 0;
  static unsigned long nextBlinkInterval = random(2000, 10000);

  if (millis() - lastBlink >= nextBlinkInterval) {
    blink_randomly();
    lastBlink = millis();
    nextBlinkInterval = random(5000, 15000);
  }

  if (isEmotionActive) {
    execute_emotion(activeEmotion);
  }

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "STOP_EMOTION") {
      stop_emotion();
      return;
    }

    if (isEmotionActive) {
      Serial.println("Vykonáva sa emócia!");
      return;
    }

    if (input == "HELLO NICO") {
      Serial.println("HELLO FROM NICO");
      return;
    } 

    int colonIndex = input.indexOf(':');

    if (colonIndex != -1) {
      String command = input.substring(0, colonIndex);
      String value = input.substring(colonIndex + 1);
      Serial.println("Command: " + command + ", Value: " + value);

      if (command.equals("EMOTION")) {
        start_emotion(value);
      } else if (command.equals("TURN_ON")) {
        command_turn_on(value);
      } else if (command.equals("TURN_OFF")) {
        command_turn_off(value);
      } else if (command.equals("EYES")) {
        command_eyes(value);
      } else if (command.equals("EYEBROWS")) {
        command_eyebrows(value);
      } else if (command.equals("MOUTH")) {
        command_mouth(value);
      } else if (command.equals("FACE")) {
        command_face(value);
      }

    } else {
      Serial.println("Unknown command!");
    }
  }
}
