import os
import shutil
import random

def classify_data():
    print("classify")

    dataset_root = './subpicture'
    train_dir = './train'
    val_dir = './val'
    # test_dir = './test'


    shutil.rmtree(train_dir)
    shutil.rmtree(val_dir)
    # shutil.rmtree(test_dir)

    train_ratio = 0.8
    val_ratio = 0.2
    # test_ratio = 0.2

    for person_folder in os.listdir(dataset_root):
        person_path = os.path.join(dataset_root, person_folder)
        
        if os.path.isdir(person_path):
            # 获取个人图片列表
            person_images = [f for f in os.listdir(person_path) if f.endswith('.jpg') or f.endswith('.png')]
            random.shuffle(person_images)
            
            # 计算划分边界
            num_images = len(person_images)
            num_train = int(train_ratio * num_images)
            # num_val = int(val_ratio * num_images)
            
            # 划分图片
            train_images = person_images[:num_train]
            # val_images = person_images[num_train:num_train + num_val]
            # test_images = person_images[num_train + num_val:]
            val_images = person_images[num_train:]
            
            # 创建目标文件夹并将图片复制过去
            os.makedirs(os.path.join(train_dir, person_folder), exist_ok=True)
            os.makedirs(os.path.join(val_dir, person_folder), exist_ok=True)
            # os.makedirs(os.path.join(test_dir, person_folder), exist_ok=True)
            
            for img in train_images:
                shutil.copy(os.path.join(person_path, img), os.path.join(train_dir, person_folder, img))
            for img in val_images:
                shutil.copy(os.path.join(person_path, img), os.path.join(val_dir, person_folder, img))
            # for img in test_images:
                # shutil.copy(os.path.join(person_path, img), os.path.join(test_dir, person_folder, img))
