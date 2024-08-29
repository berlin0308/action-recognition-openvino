import numpy as np
import os
import tensorflow as tf
from PIL import Image
import random

frames = 16
classes = 11
res = 224
aug = False



def preprocess_image(filename, res):
    """Use Pillow to open and preprocess an image, returning as a TensorFlow tensor."""
    # Open the image file with Pillow
    img = Image.open(filename.numpy().decode('utf-8'))
    img = img.resize((res, res))
    img_array = np.array(img)
    img_array = img_array / 255.0
    return img_array

def augment_image(image, res):
    """Apply random transformations to augment image data."""

    if random.randint(0, 1) == 1: # 50% augmentation
        image = tf.image.resize(image, [int(res * 1.1), int(res * 1.1)])
        image = tf.image.random_crop(image, size=[res, res, 3])
    
    if random.randint(0, 1) == 1: # 50% augmentation
        image = tf.image.random_brightness(image, max_delta=0.1)
    if random.randint(0, 1) == 1: # 50% augmentation
        image = tf.image.random_contrast(image, lower=0.9, upper=1.1)
    if random.randint(0, 1) == 1: # 50% augmentation
        image = tf.image.random_saturation(image, lower=0.9, upper=1.1)
    
    return image

def tf_preprocess_image(filename, res):
    """Wrap preprocess_image using tf.py_function to handle tensor inputs."""
    [image] = tf.py_function(preprocess_image, [filename, res], [tf.float32])
    image.set_shape((res, res, 3))

    if aug:
        image = augment_image(image, res) 
    
    return image

def load_and_preprocess_video(file_paths):
    """Process each video using TensorFlow operations."""
    video = tf.map_fn(lambda x: tf_preprocess_image(x, res), file_paths, fn_output_signature=tf.float32)
    return video

def process_path(video_folder, label):

    wildcard_path = tf.strings.join([video_folder, '/*.jpg'])

    video_files = tf.io.matching_files(wildcard_path)

    video_files = video_files[:frames]

    print(len(video_files))
    # assert len(video_files) == 16

    video = load_and_preprocess_video(video_files)
    label = tf.one_hot(label, depth=classes)

    return video, label


def create_complete_dataset(root_folder, batch_size=1, resolution=224, shuffle=False, augmentation=False, oversample=False, target_samples_per_class=100):
    global res
    res = resolution

    global aug
    aug = augmentation

    label_map = ["0_Background","1_Entry","2_Bag_Operation","3_Machine_Operation","4_Item_Pickup","5_Normal_Scanning","6_Abnormal_Scanning_Skipping","7_Abnormal_Scanning_TwoAtATime","8_Abnormal_Scanning_CoverUp","9_Abnormal_Scanning_HidingBehind","10_Leaving"]

    label_dict = {label: index for index, label in enumerate(label_map)}

    video_folders = []
    labels = []

    for class_name, label in label_dict.items():
        # print(class_name, label)

        class_path = os.path.join(root_folder, class_name)
        videos = [os.path.join(class_path, video_folder) for video_folder in sorted(os.listdir(class_path))]
        count = len(videos)

        if oversample: # 1800
            repeat_factor = target_samples_per_class // count + (1 if target_samples_per_class % count != 0 else 0)
            videos = videos * repeat_factor  # Repeat the list to ensure we have enough samples
            video_folders.extend(videos[:target_samples_per_class])  # Limit to the target size
            labels.extend([label] * target_samples_per_class)
        else:
            video_folders.extend(videos)
            labels.extend([label] * len(videos))

            

    if shuffle:
        combined = list(zip(video_folders, labels))
        random.shuffle(combined)
        video_folders, labels = zip(*combined)
        video_folders = list(video_folders)
        labels = list(labels)

    video_folders = tf.data.Dataset.from_tensor_slices(video_folders)
    labels = tf.data.Dataset.from_tensor_slices(labels)
    dataset = tf.data.Dataset.zip((video_folders, labels))
    dataset = dataset.map(process_path)  # Use process_path to handle video and labels

    # if shuffle:
    #     dataset = dataset.shuffle(buffer_size=100, reshuffle_each_iteration=True)

    dataset = dataset.batch(batch_size)

    return dataset





# train_dataset = create_complete_dataset('data/V1.1/train', augmentation=True, batch_size=1, resolution=224, shuffle=True, oversample=True, target_samples_per_class=100)

# print(len(train_dataset))
# for features, targets in train_dataset.take(10):
#   print ('Features: {}, Target: {}'.format(features.shape, targets, targets.shape))
