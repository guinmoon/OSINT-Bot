import base64
import random
import re
import string

import numpy as np
import pytesseract
import cv2

from python3_anticaptcha import  ImageToTextTask


class CaptchaDecode:
    def __init__(self,anticaptcha_key=''):
        self.anticaptcha_key= anticaptcha_key
        pass
    
    def save_image(self,response):
        image_b64 = response['result']['image']
        image_data = self.decode_b64(image_b64)
        path = self.generate_random_name()
        self.write_data_image(image_data, path)
        return path

    def decode_response(self, response):
        path = self.save_image(response)
        return self.decrypt(path), path

    def decode_response_manual(self, response):
        path = self.save_image(response)
        return path

    def decode_response_anticaptcha(self,response):
        anticaptcha_key = self.anticaptcha_key
        path = self.save_image(response)
        user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = anticaptcha_key).captcha_handler(captcha_file=path)
        return user_answer["solution"]["text"], path
    
    @staticmethod
    def decode_path(self, path):
        return self.decrypt(path)

    @staticmethod
    def generate_random_name():
        return 'captcha/' + ''.join([random.choice(string.ascii_letters) for _ in range(10)]) + '.jpg'

    @staticmethod
    def write_data_image(data, path):
        with open(path, 'wb') as f:
            f.write(data)

    @staticmethod
    def decode_b64(data):
        return base64.b64decode(data)

    @staticmethod
    def decrypt(path):
        frame = cv2.imread(path)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([30, 120, 0]), np.array([255, 255, 255]))
        text = pytesseract.image_to_string(mask)
        text = re.sub("[^A-Za-z0-9]", '', text)
        return text

    @staticmethod
    def decrypt_anticaptcha(path):
        frame = cv2.imread(path)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, np.array([30, 120, 0]), np.array([255, 255, 255]))
        text = pytesseract.image_to_string(mask)
        text = re.sub("[^A-Za-z0-9]", '', text)
        return text
