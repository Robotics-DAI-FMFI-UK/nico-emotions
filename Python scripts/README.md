# Python programy

Táto časť repozitára obsahuje vytvorené ovládače **Controllers** pre robotickú tvár, interaktívny generátor variácií emócií **position_generator**, GUI pre emócie a konkrétne príklady využitia ovládačov (**face_tracker**, **dino_recognition**, **distances_filter**).   

### Maximálna verzia Python 3.11

## Potrebné knižnice

Controllers:
- math
- numpy
- os
- pyrealsense2
- serial
- time
- requests

Position_generator:
- math
- os
- pillow
- time

Face_tracker:
- opencv-python

Dino_recognition:
- opencv-python
- numpy
- onnxruntime
- os
- requests

Distances_filter:
- opencv-python
- numpy
- time

Všetky si je možné nainštalovať naraz príkazom:
```
python -m pip install numpy pyrealsense2==2.54.2.5684 serial requests pillow opencv-python onnxruntime
```
V prípade, že máte viacero verzií pythonu, v príkaze prosím `python` nahraďte adekvátnou verziou napr. `python3.11`. 

## Problém inštalácie pyrealsense2

Pri inštalovaní knižnice pyrealsense2 sme narazili na problém, ktorý spomalil náš postup. Jednalo sa o chybu: "RuntimeError: failed to convert special folder: errno=42". Po dlhom pátraní sme sa dočítali, že je to chyba verzie a preto odporúčame použiť staršiu verziu - `pip install pyrealsense2==2.54.2.5684`.


## Použitie ovládačov

Ovládače sa importujú zo zložky **Controllers**, pričom stačí použiť len FaceController a RealSenseCamera, zvyšné časti sú poprepájané. Nastavenia a preferencie je možné meniť v **Controllers/config.py**.
```
from Controllers.face_controller import FaceController 
from Controllers.realsense_camera import RealSenseCamera
```

## Generátor emócií

Generátor stačí len zapnúť a vykresliť. Má prednastavené variácie emócií a dokáže z nich vygenerovať rôzne obrázky. Pri chybe programu alebo inej komplikácií je možné znovu vygenerovať všetky konfigurácie. Je tam nastavený cooldown 1s na každý obrázok, preto pri veľa obrázkoch je potrebné si chvíľu počkať.
