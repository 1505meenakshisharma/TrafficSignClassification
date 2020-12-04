from django.shortcuts import render
import tensorflow as tf
from PIL import Image
import io
import numpy as np
import base64

def image_processing(img):
    model = tf.keras.models.load_model('./model/Traffic_Sign_Classification_CNN_Model.h5')
    data = []
    image = Image.open(io.BytesIO(img))
    image_extension = image.format
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    #For predicting the class label of uploaded traffic sign image
    image_to_predict = image.resize((50, 50), Image.LANCZOS)
    data.append(np.array(image_to_predict))
    x_test = np.array(data)
    y_pred = model.predict_classes(x_test)

    #For previewing the uploaded image in the browser
    image_to_preview = image.resize((246, 246), Image.LANCZOS)
    image_to_preview_in_bytes = io.BytesIO()
    image_to_preview.save(image_to_preview_in_bytes, format = image_extension)
    image_to_preview_in_bytes = image_to_preview_in_bytes.getvalue()

    #Encode the bytes-like object using base64.b64encode() and return the encoded bytes (ASCII characters
    #within b'' i.e., of bytes class type) which is again decoded using decode('utf-8') to just remove b''
    #and get only ASCII characters which then will be of string class type
    #Note :- Output class type using base64.b64encode() always yield same class type which is there in input
    image_to_preview_in_string = base64.b64encode(image_to_preview_in_bytes).decode('utf-8')

    return y_pred[0], image_to_preview_in_string

def traffic_sign_classification_homepage(request):
    if request.method == 'POST':
        #Return uploaded image file as InMemoryUploadedFile class type
        traffic_sign_image = request.FILES.get('traffic_sign_image_to_search')

        #Return binary data of the uploaded image file and stored as bytes-like object
        traffic_sign_image_in_bytes = traffic_sign_image.read()

        #Classes of trafic signs
        class_labels = {    0:'Speed limit (20km/h)',
                            1:'Speed limit (30km/h)',
                            2:'Speed limit (50km/h)',
                            3:'Speed limit (60km/h)',
                            4:'Speed limit (70km/h)',
                            5:'Speed limit (80km/h)',
                            6:'End of speed limit (80km/h)',
                            7:'Speed limit (100km/h)',
                            8:'Speed limit (120km/h)',
                            9:'No passing',
                            10:'No passing for vehicles over 3.5 metric tons',
                            11:'Right-of-way at the next intersection',
                            12:'Priority road',
                            13:'Yield',
                            14:'Stop',
                            15:'No vehicles',
                            16:'Vehicles over 3.5 metric tons prohibited',
                            17:'No entry',
                            18:'General caution',
                            19:'Dangerous curve to the left',
                            20:'Dangerous curve to the right',
                            21:'Double curve',
                            22:'Bumpy road',
                            23:'Slippery road',
                            24:'Road narrows on the right',
                            25:'Road work',
                            26:'Traffic signals',
                            27:'Pedestrians',
                            28:'Children crossing',
                            29:'Bicycles crossing',
                            30:'Beware of ice/snow',
                            31:'Wild animals crossing',
                            32:'End of all speed and passing limits',
                            33:'Turn right ahead',
                            34:'Turn left ahead',
                            35:'Ahead only',
                            36:'Go straight or right',
                            37:'Go straight or left',
                            38:'Keep right',
                            39:'Keep left',
                            40:'Roundabout mandatory',
                            41:'End of no passing',
                            42:'End of no passing by vehicles over 3.5 metric tons' }
        
        key, traffic_sign_image_to_preview = image_processing(traffic_sign_image_in_bytes)
        res = "Predicted Traffic🚦Sign is : " + class_labels[key]
        return render(request, 'homepage.html', {'mime_type': traffic_sign_image.content_type, 'img': traffic_sign_image_to_preview, 'predict_result': res})
    else:
        return render(request, 'homepage.html')