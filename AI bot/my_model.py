from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
from ultralytics import YOLO

model_path="C:\Users\Администратор\Desktop\AI bot\Converted_keras\keras_model.h5"
labels_path="C:\Users\Администратор\Desktop\AI bot\Converted_keras\labels.txt"

def detect_deapfake_or_real_person(image_path):
    try:
        detector = YOLO("yolov8n.pt")
        results = detector(image_path)
        objects = results[0].boxes.cls.cpu().numpy() 
        if not any(cls in [0] for cls in objects):
            return f"Извините, я не уверен, что это на картинке. Человек не найден."
        np.set_printoptions(suppress=True)
        model = load_model("keras_model.h5", compile=False)
        class_names = open("labels.txt", "r").readlines()
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(image_path).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]


        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)

    except Exception:
        return f"Ошибка при анализе изображения: {str(Exception)}"


detect_deapfake_or_real_person()