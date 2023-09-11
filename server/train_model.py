import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.models import Sequential


def train():

    print("retrain")
    # 数据集路径和参数
    train_dir = './train'
    val_dir = './val'
    # test_dir = './test'
    image_size = (128, 128)
    batch_size = 32
    num_classes = len(os.listdir(train_dir))
    print(num_classes)

    train_datagen = ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1.0/255)
    # test_datagen = ImageDataGenerator(rescale=1.0/255)

    # 加载数据集
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    # test_generator = test_datagen.flow_from_directory(
    #     test_dir,
    #     target_size=image_size,
    #     batch_size=batch_size,
    #     class_mode='categorical'
    # )

    # 构建模型
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(image_size[0], image_size[1], 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        # Dense(64, activation='relu'),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    # 编译模型
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    # 训练模型
    model.fit(train_generator, epochs=10, validation_data=val_generator)

    model.save('face_recognize.h5')