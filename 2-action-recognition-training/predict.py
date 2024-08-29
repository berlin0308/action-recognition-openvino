import tensorflow as tf
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
from datetime import datetime
import json
import cv2

res = 224


def preprocess_image(filename, res):
    """Use Pillow to open and preprocess an image, returning as a TensorFlow tensor."""
    # Open the image file with Pillow
    img = Image.open(filename.numpy().decode('utf-8'))
    img = img.resize((res, res))
    img_array = np.array(img)
    img_array = img_array / 255.0
    return img_array

def tf_preprocess_image(filename, res):
    """Wrap preprocess_image using tf.py_function to handle tensor inputs."""
    [image] = tf.py_function(preprocess_image, [filename, res], [tf.float32])
    image.set_shape((res, res, 3))

    # img_processed = tf.expand_dims(image, axis=0)
    # img_processed = tf.expand_dims(img_processed, axis=0)
    
    return image

def load_and_preprocess_video(file_paths):
    """Process each video using TensorFlow operations."""
    video = tf.map_fn(lambda x: tf_preprocess_image(x, res), file_paths, fn_output_signature=tf.float32)
    return video



def predict_behavior(runner=None, resolution=172, mp4_file_path=None, jpg_folder_path=None, input_state=None, output_state=False, saved_model=None
                    , update_stride=0, output_images=False, config_file_path=None):

    x1, y1, x2, y2 = 0, 0, 0, 0
    if config_file_path is not None:
        with open(config_file_path, 'r') as file:
            config = json.load(file)
        x1, y1, x2, y2 = config['x1'], config['y1'], config['x2'], config['y2']


    global res
    res = resolution
    # print(res)

    # print(saved_model)

    if input_state is not None:
        init_states = input_state


    if mp4_file_path is not None:
        mv_clip = VideoFileClip(mp4_file_path)
        # mv_clip = mv_clip.resize((res,res))

        fps = mv_clip.fps
        resolution = mv_clip.size
        duration = mv_clip.duration

        print(f"FPS: {fps}, Res: {resolution[0]}x{resolution[1]}, Duration: {duration}")


        video = [] # model input
        clip = [] # displayed image

        for frame in mv_clip.iter_frames(fps=10):
            img = Image.fromarray(frame)

            if config_file_path is not None:
                img = img.resize((1920, 1280))
            else:
                img = img.resize((res, res))

            img_array = np.array(img, dtype=np.float32)
            img_array = img_array / 255.0
            
            # print(img_array.shape)
            clip.append(img_array)

            if config_file_path is not None:
                img_array = img_array[y1:y2, x1:x2]
                img_array = cv2.resize(img_array, (224, 224))


            img_processed = tf.expand_dims(img_array, axis=0)
            img_processed = tf.expand_dims(img_processed, axis=0)

            # print(img_processed.shape)
            # print(img_processed.dtype)

            video.append(img_processed)


    elif jpg_folder_path is not None:

        wildcard_path = tf.strings.join([jpg_folder_path, '/*.jpg'])

        video_files = tf.io.matching_files(wildcard_path)

        video = load_and_preprocess_video(video_files)
        # print(len(video))
        


    """
    Start Predicting...
    """

    states = init_states.copy()
    all_logits = []
    start = datetime.now()

    # print(len(video))
    
    for frame_i, frame in enumerate(video):

        # Input shape: [1, 1, res, res, 3]
        # print(frame.shape)

        if update_stride != 0 and (frame_i % update_stride ==0):
            states = init_states.copy()
            # print(f"States updated at {frame_i}")

        if saved_model is not None:
            outputs = saved_model(**states, image=frame)
            logits = outputs.pop('logits')[0]

        # print(logits)
        all_logits.append(logits)

        states = outputs

    end = datetime.now()

    print(f"Inference Time: {end-start}")

    
    # print(all_logits)
    # print(logits) # [-40 -33 -29 -21 -58 -46 -29] -> max: -21
    probs = tf.nn.softmax(tf.cast(logits, dtype='float'))
    # print(probs)


    if mp4_file_path is not None:
        if output_images:
            return probs, all_logits, clip

        clip_np = tf.stack(clip).numpy()
        # print(clip_np.shape)
        if output_state:
            return probs, all_logits, clip_np, states
        return probs, all_logits, clip_np

    if jpg_folder_path is not None:
        return probs, all_logits