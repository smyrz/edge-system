from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import cross_origin
import time
import sqlite3
import os
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import standardize_picture
import train_model
import classify_data
from concurrent.futures import ThreadPoolExecutor

# app初始化
app = Flask(__name__)
 
executor = ThreadPoolExecutor(3)

# recevie picture and classify wether is a stranger and send result and recevie more and retrain

@app.route("/upload", methods=["POST","GET"])
def upload_image():
    imageData = request.get_data(parse_form_data=False)

    filename = time.strftime("%m%d%H%M%S", time.localtime()) + ".jpg"
    path = "./temp/" + str(filename)
    file = open(path, "wb")
    file.write(imageData)

    return jsonify({'msg': 'success'})

@app.route("/recognize", methods=["GET"])
def recognize_image():
    path = "C:/Users/smyrz1/Desktop/project/temp/"
    index = recognize()
    if index != 0:
        print(type(index))
        conn = sqlite3.connect('face_recognize.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO PERSON_RECORD (person_id) VALUES (?)', (int(index),))
        
        conn.commit()
        conn.close()
        del_list = os.listdir(path)
        # for f in del_list:
        #     file_path = os.path.join(path, f)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        #     elif os.path.isdir(file_path):
        #         shutil.rmtree(file_path)
        return jsonify({'msg': 'familiar'})
    return jsonify({'msg': 'stranger'})


def recognize():
    print("face recognize")

    path = "C:/Users/smyrz1/Desktop/project/temp/"

    # standardize
    standardize_picture.standardizebatch(path)

    for person_folder in os.listdir(path):
        path = os.path.join(path, person_folder)
        break
    print("revognize" + path)
    loaded_model = load_model('./face_recognize.h5')

    image = load_img(path, target_size=(128, 128))
    image_array = img_to_array(image) / 255.0  

    image_batch = np.expand_dims(image_array, axis=0)
    predictions = loaded_model.predict(image_batch)
    class_index = np.argmax(predictions[0])
    print("perdicet " + str(class_index))
    return class_index


@app.route('/')
def index():
    # 查询数据，包括存入时间
    conn = sqlite3.connect('face_recognize.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PERSON_RECORD')
    persons = cursor.fetchall()
    for person in persons:
        print(person)
    path = "C:/Users/smyrz1/Desktop/project/temp"
    image_exists = False
    if len(os.listdir(path)) != 0:
        image_exists = True
    return render_template('index.html', image_exists = image_exists)

@app.route('/show_records')
def show_records():
    # 查询数据，包括存入时间
    conn = sqlite3.connect('face_recognize.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pr.record_id, p.name, pr.created_time FROM PERSON_RECORD pr left join PERSON p on pr.person_id = p.person_id LIMIT 20')

    rows = cursor.fetchall()
    print(rows)
    return render_template('show.html', rows = rows)

@app.route('/show_image', methods=['GET'])
def show_image():
    # 在这里添加显示图片的逻辑
    path = "C:/Users/smyrz1/Desktop/project/temp"

    for person_folder in os.listdir(path):
        path = os.path.join(path, person_folder)
        break
    return send_file(path, mimetype='image/jpg')


# record the person coming
@app.route('/add_person', methods=['POST'])
def add_person():
    picture_file_dir = 'C:/Users/smyrz1/Desktop/project/subpicture'


    dir_list = os.listdir(picture_file_dir)
    index = len(dir_list)
    name = request.form.get('name')
    path = "C:/Users/smyrz1/Desktop/project/subpicture/" + str(index) + name
    os.mkdir(path)

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    conn = sqlite3.connect('face_recognize.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO PERSON (name, picture_path) VALUES (?, ?)', (name, path,))

    cursor.execute('INSERT INTO PERSON_RECORD (person_id) VALUES (?)', (index,))

    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    origin_path = "C:/Users/smyrz1/Desktop/project/temp"

    # standardize
    standardize_picture.standardizebatch(origin_path)

    filelist = os.listdir(origin_path)     
    for file in filelist:
        src = os.path.join(origin_path, file)
        dst = os.path.join(path, file)
        print('src:', src)                 # 原文件路径下的文件
        print('dst:', dst)                 # 移动到新的路径下的文件
        shutil.move(src, dst)

    classify_data.classify_data()
    executor.submit(train_model.train)
    return jsonify({'message': 'added to the database'}), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,)   
