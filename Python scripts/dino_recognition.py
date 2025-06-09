import numpy as np
import os
import requests
import onnxruntime as ort
import cv2 as cv
from Controllers.face_controller import FaceController 
from Controllers.realsense_camera import RealSenseCamera

ESC = 27
ENTER = 13

def download_and_save(url,path):
    if os.path.exists(path):
        return
    print("downloading",path)
    response = requests.get(url)
    open(path,"wb").write(response.content)
    print(path,"downloaded")
    
def download_DinoViT_model():
    download_and_save("https://www.agentspace.org/download/dino_deits8-224-final.onnx","dino_deits8-224-final.onnx")

download_DinoViT_model()

providers = ['CUDAExecutionProvider' if ort.get_device() == 'GPU' else 'CPUExecutionProvider']
session = ort.InferenceSession("dino_deits8-224-final.onnx", providers=providers)
input_names = [input.name for input in session.get_inputs()] 
output_names = [output.name for output in session.get_outputs()] 

def dino(image):
    image_size = (224, 224)
    blob = cv.dnn.blobFromImage(image, 1.0/255, image_size, swapRB=True, crop=True)
    blob[0][0] = (blob[0][0] - 0.485)/0.229
    blob[0][1] = (blob[0][1] - 0.456)/0.224
    blob[0][2] = (blob[0][2] - 0.406)/0.225
            
    data_input = { input_names[0] : blob }
    data_output = session.run(output_names, data_input)
    features = data_output[0][0]
    attentions = data_output[1][0]

    nh = attentions.shape[0]
    attentions = attentions[:, 0, 1:].reshape(nh, -1)
    patch_size = 8
    w_featmap, h_featmap = image_size[0] // patch_size, image_size[1] // patch_size
    attentions = attentions.reshape(nh, w_featmap, h_featmap)

    points = []
    for i, attention in enumerate(attentions):
        attention /= np.max(attention)
        attention = np.asarray(attention*255,np.uint8)
        _, featmap = cv.threshold(attention,0,255,cv.THRESH_BINARY|cv.THRESH_OTSU)

        if i == 2:
            mask = cv.resize(attention,(image.shape[1],image.shape[0]))
        
        indices = np.where(featmap > 0)
        if len(indices[1]) > 0 and len(indices[0]) > 0:
            point = (np.average(indices[1])/w_featmap,np.average(indices[0])/h_featmap)
        else:
            point = None
        
        points.append(point),

    return mask, points, features

def dino_visualization(frame, mask, points):
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    result = cv.merge([gray,gray,gray|mask])
    for i, point in enumerate(points):
        if point is not None:
            pt = (int(point[0]*frame.shape[1]),int(point[1]*frame.shape[0]))
            cv.circle(result,pt,3,(0,0 if i == 2 else 255,255),cv.FILLED)
            cv.putText(result,str(i),(pt[0],pt[1]-5),0,1.0,(0,0 if i == 2 else 255,255),2)

    return result
    
if __name__ == "__main__": 
    camera = RealSenseCamera()
    face = FaceController()

    tracking = False
    tracked_point = None
    delta_threshold = 50

    try:
        while True:

            frame = camera.get_color_frame()
            if frame is None:
                continue

            cv.imshow('input', frame)
            key = cv.waitKey(1)

            if key == ENTER:
                tracking = True
                face.turn_part("ON", "EYES")

            if key == ESC:
                if not tracking:
                    break

                tracking = False
                face.turn_part("OFF", "EYES")
                tracked_point = None

            if tracking:
                mask, points, _ = dino(frame)
                second_point = points[1]
                
                if second_point is not None:
                    new_point = (int(second_point[0] * frame.shape[1]), int(second_point[1] * frame.shape[0]))

                    if tracked_point is None or abs(new_point[0] - tracked_point[0]) > delta_threshold or abs(new_point[1] - tracked_point[1]) > delta_threshold:
                        tracked_point = new_point

                    distance = camera.get_distance(tracked_point)
                    object_center = camera.get_eyes_point([tracked_point[0], tracked_point[1], distance, 1])

                    cv.circle(frame, tracked_point, 5, (0, 0, 255), cv.FILLED)
                    cv.putText(frame, f"{object_center[0]}, {object_center[1]}, {object_center[2]}", (tracked_point[0], tracked_point[1] - 5), 0, 0.5, (0, 0, 255), 2)
                    face.look_at(object_center)

            cv.imshow('DINO', frame)

    finally:
        face.close_connection()
        camera.stop()
        cv.destroyAllWindows()

