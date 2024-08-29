from moviepy.editor import *
from moviepy import *
import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# labeled data path
DATA_LABELED_ROOT =      'data/V1.2/V1.2_mp4'
# new folder for preprocessed data
DATA_PREPROCESSED_ROOT = 'data/V1.2/V1.2_jpgs'


size = 224
num_frames = 16


def iterate_mp4_files(root_path):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".mp4") and not file.startswith("._"):
                file_path = os.path.join(root, file)
                yield file_path

def preprocess_label_mp4():
    # build new path for preprocessed data
    for labeled_class in os.listdir(DATA_LABELED_ROOT):
        os.makedirs(os.path.join(DATA_PREPROCESSED_ROOT,labeled_class), mode=0o777, exist_ok=True)


    for labeled_class in os.listdir(DATA_LABELED_ROOT):
        CLASS_ROOT = os.path.join(DATA_LABELED_ROOT,labeled_class)
        print("Start to process -- "+CLASS_ROOT)
        for mp4_file_path in iterate_mp4_files(CLASS_ROOT):
            print("Read: "+mp4_file_path)

            processed_clip_path = os.path.join(DATA_PREPROCESSED_ROOT,labeled_class, os.path.splitext(os.path.basename(mp4_file_path))[0])

            clip = VideoFileClip(mp4_file_path)
            clip = clip.resize((size,size))
            

            os.makedirs(processed_clip_path, mode=0o777, exist_ok=True)
            
            total_frames = clip.reader.nframes
            # print(total_frames)

            # num_images = 0
            for i, frame in enumerate(clip.iter_frames()):
                if i <= num_frames-1: 
                    img = ImageClip(frame)
                    img.save_frame(processed_clip_path+f"/image_{i:05d}.jpg")
                    # num_images = i
                    # print(num_images)
            
            # assert num_images == 15


if __name__ == '__main__':

    os.makedirs(DATA_PREPROCESSED_ROOT, mode=0o777, exist_ok=True)

    preprocess_label_mp4()

    # with ThreadPoolExecutor(max_workers=8) as executor:
    #     for mp4_file_path in iterate_mp4_files(DATA_LABELED_ROOT):
    #         executor.submit(process_mp4_files, mp4_file_path)



