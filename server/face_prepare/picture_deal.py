import os
from PIL import Image
import glob
import cv2
import shutil
picture_file_dir = 'C:/Users/smyrz1/Desktop/project/subpicture'


dir_list = os.listdir(picture_file_dir)
print(dir_list)
# for people in dir_list:
#     people_dir = os.path.join(picture_file_dir, people)
#     for img_name in os.listdir(people_dir):
#         img_path = people_dir + '/' + img_name
#         print(img_path)
#         img = Image.open(img_path)
#         img.thumbnail((500,500))
#         print(img.format, img.size, img.mode)
#         img.save(img_path,'JPEG')


origin_path = "C:/Users/smyrz1/Desktop/project/temp"
os.mkdir("C:/Users/smyrz1/Desktop/project/temp/test")
filelist = os.listdir(origin_path)     
print(filelist)
for file in filelist:
    src = os.path.join(origin_path, file)
    dst = os.path.join("C:/Users/smyrz1/Desktop/project/temp/test", file)
    print('src:', src)                 # 原文件路径下的文件
    print('dst:', dst)                 # 移动到新的路径下的文件
    shutil.move(src, dst)
