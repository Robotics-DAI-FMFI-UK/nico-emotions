# Program riadiacej jednotky

Tento kód bol navrhnutý pre použitie mikrokontroléra Raspberry Pi Pico 2. Program sme vyvíjali v prostedí Arduino IDE s rozšírením board manager [Arduino-Pico](https://github.com/earlephilhower/arduino-pico/). 

## Inštalácia rozšírenia
1. Treba otvoriť File -> Preferences
2. Do "Additional boards manager URLs" treba pridať:
https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
3. V paneli "Boards manager" stačí vyhľadať "Raspberry Pi Pico"
4. Install

Pri inštalácií na windows je potrebné si dať pozor na pomenovanie účtu, pretože rozšírenie nedokáže korektne rozlišovať diakritiku v mene.

## Vlastné definovanie emócií

Predom sme definovali iba základné emócie. Ak má užívateľ vlastné preferencie, je potrebné zájsť do súboru **Emotions.cpp** a **Emotions.h**. Pri definovní novej emócie sú potrebné nasledovné kroky:

1. V **Emotions.cpp** vytvoríme nové pole pomenované podľa emócie a definujeme jednotlivé kroky emócie - {načasovanie, natočenia motorčekov}
2. V tom istom súbore pridáme do funkcie void Emotions::initialize() nové definície emócie:
    emotionMap[emotionCount].name = "NOVÁ EMÓCIA";
    emotionMap[emotionCount].data = nova_emocia;
    emotionMap[emotionCount++].steps = nova_emocia_steps;
3. Do súboru **Emotions.h** zapíšeme novú premennú *extern int nova_emocia[][nova_emocia_steps]*;
4. Zvýšime počítadlo *#define EMOTIONS_COUNT i+1*
5. Upravený kód nahráme do mikrokontroléra

Tento postup je zdĺhavý, preto ak nastane ďalšie rozširovanie práce, pridávanie vlastných emócií sa zlepší.

## Potrebné knižnice
- Arduino
- OneWire
- DallasTemperature