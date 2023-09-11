import cv2
import dlib
import os

def standardizebatch(path):
    
    print("standardizebatch")

    detector = dlib.get_frontal_face_detector()
    
    for person_folder in os.listdir(path):
        person_path = os.path.join(path, person_folder)
        print(person_path)
    
        img   = cv2.imread(person_path)#读取数据

        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 使用detector进行人脸检测
        dets = detector(gray_img, 1)

        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0

            face = img[x1:y1,x2:y2]

            face = cv2.resize(face, (128,128))

            cv2.imshow('image', face)

            cv2.imwrite(person_path, face)

def standardize(person_path):

    print("standardize " + person_path)
    #使用dlib自带的frontal_face_detector作为我们的特征提取器
    detector = dlib.get_frontal_face_detector()

    img   = cv2.imread(person_path)#读取数据
    # 转为灰度图片
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用detector进行人脸检测
    dets = detector(gray_img, 1)

    for i, d in enumerate(dets):
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0

        face = img[x1:y1,x2:y2]

        face = cv2.resize(face, (128,128))

        cv2.imshow('image', face)

        cv2.imwrite(person_path, face)
