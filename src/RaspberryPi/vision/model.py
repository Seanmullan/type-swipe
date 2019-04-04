#import tensorflow as tf
import numpy as np
import time
import cv2
from keras.applications.vgg16 import VGG16
from keras.layers import Input
from keras.engine.topology import Container
from keras.models import Model
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.models import Sequential
from keras.preprocessing import image 
from keras.preprocessing.image import img_to_array
from keras import optimizers

class VisionModel():
    """
    Invokes machine learning model to classify image as containing a metal, glass or
    plastic object.
    """

    def __init__(self):
        self.model = self.initialise()
        self.model._make_predict_function()
        print "[MODEL] Initialised"

    def initialise(self):
        """
        Initialises machine learning model paramaters.
        """
        print "[MODEL] Initialising..."
        top_model = load_model('/home/student/vision/vgg_top_model.h5')
        input_tensor = Input(shape=(150, 150,3))
        base_model = VGG16(weights='imagenet',include_top= False,input_tensor=input_tensor)
        model = Model(inputs= base_model.input, outputs= top_model(base_model.output))
        model.compile(loss='categorical_crossentropy',
                        optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                        metrics=['accuracy'])
        return model

    def predict(self,img):
        """
        Returns class with maximum psoterior probability.
        """
        img_data = self.preprocess(img)
        output=self.model.predict(img_data)
        return np.argmax(output)

    def preprocess(self,img):
        """
        Converts image to gray scale and reshapes to (150,150,3).
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        stacked_img = np.stack((gray,)*3, axis=-1)

        x=cv2.resize(stacked_img, dsize=(150, 150), interpolation=cv2.INTER_CUBIC)
        x=np.array(x,dtype="float32")
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        img_data = np.array([x])
        img_data=np.rollaxis(img_data,1,0)
        return img_data[0]
