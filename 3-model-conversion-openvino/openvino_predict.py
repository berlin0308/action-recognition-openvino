import tensorflow as tf
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
from datetime import datetime


image_mean = np.array([0.40742482, 0.41668848, 0.39488508], dtype=np.float32)
image_std = np.array([0.2889984, 0.28819978, 0.28711625], dtype=np.float32)


output_to_input_map = {
    'StatefulPartitionedCall:54': 'call_state_block4_layer1_pool_frame_count:0',
    'StatefulPartitionedCall:11': 'call_state_block1_layer1_stream_buffer:0',
    'StatefulPartitionedCall:14': 'call_state_block1_layer2_stream_buffer:0',
    'StatefulPartitionedCall:37': 'call_state_block3_layer1_pool_frame_count:0',
    'StatefulPartitionedCall:39': 'call_state_block3_layer2_pool_buffer:0',
    'StatefulPartitionedCall:32': 'call_state_block2_layer4_stream_buffer:0',
    'StatefulPartitionedCall:43': 'call_state_block3_layer3_pool_frame_count:0',
    'StatefulPartitionedCall:50': 'call_state_block4_layer0_pool_buffer:0',
    'StatefulPartitionedCall:67': 'call_state_head_pool_frame_count:0',
    'StatefulPartitionedCall:59': 'call_state_block4_layer4_pool_buffer:0',
    'StatefulPartitionedCall:35': 'call_state_block3_layer0_stream_buffer:0',
    'StatefulPartitionedCall:26': 'call_state_block2_layer2_stream_buffer:0',
    'StatefulPartitionedCall:63': 'call_state_block4_layer5_stream_buffer:0',
    'StatefulPartitionedCall:21': 'call_state_block2_layer1_pool_buffer:0',
    'StatefulPartitionedCall:23': 'call_state_block2_layer1_stream_buffer:0',
    'StatefulPartitionedCall:38': 'call_state_block3_layer1_stream_buffer:0',
    'StatefulPartitionedCall:51': 'call_state_block4_layer0_pool_frame_count:0',
    'StatefulPartitionedCall:16': 'call_state_block1_layer3_pool_frame_count:0',
    'StatefulPartitionedCall:29': 'call_state_block2_layer3_stream_buffer:0',
    'StatefulPartitionedCall:62': 'call_state_block4_layer5_pool_frame_count:0',
    'StatefulPartitionedCall:60': 'call_state_block4_layer4_pool_frame_count:0',
    'StatefulPartitionedCall:44': 'call_state_block3_layer3_stream_buffer:0',
    'StatefulPartitionedCall:9': 'call_state_block1_layer1_pool_buffer:0',
    'StatefulPartitionedCall:40': 'call_state_block3_layer2_pool_frame_count:0',
    'StatefulPartitionedCall:1': 'call_state_block0_layer0_pool_buffer:0',
    'StatefulPartitionedCall:3': 'call_state_block0_layer1_pool_buffer:0',
    'StatefulPartitionedCall:2': 'call_state_block0_layer0_pool_frame_count:0',
    'StatefulPartitionedCall:30': 'call_state_block2_layer4_pool_buffer:0',
    'StatefulPartitionedCall:7': 'call_state_block1_layer0_pool_frame_count:0',
    'StatefulPartitionedCall:4': 'call_state_block0_layer1_pool_frame_count:0',
    'StatefulPartitionedCall:33': 'call_state_block3_layer0_pool_buffer:0',
    'StatefulPartitionedCall:25': 'call_state_block2_layer2_pool_frame_count:0',
    'StatefulPartitionedCall:19': 'call_state_block2_layer0_pool_frame_count:0',
    'StatefulPartitionedCall:61': 'call_state_block4_layer5_pool_buffer:0',
    'StatefulPartitionedCall:56': 'call_state_block4_layer2_pool_frame_count:0',
    'StatefulPartitionedCall:10': 'call_state_block1_layer1_pool_frame_count:0',
    'StatefulPartitionedCall:27': 'call_state_block2_layer3_pool_buffer:0',
    'StatefulPartitionedCall:41': 'call_state_block3_layer2_stream_buffer:0',
    'StatefulPartitionedCall:52': 'call_state_block4_layer0_stream_buffer:0',
    'StatefulPartitionedCall:8': 'call_state_block1_layer0_stream_buffer:0',
    'StatefulPartitionedCall:36': 'call_state_block3_layer1_pool_buffer:0',
    'StatefulPartitionedCall:46': 'call_state_block3_layer4_pool_frame_count:0',
    'StatefulPartitionedCall:65': 'call_state_block4_layer6_pool_frame_count:0',
    'StatefulPartitionedCall:57': 'call_state_block4_layer3_pool_buffer:0',
    'StatefulPartitionedCall:6': 'call_state_block1_layer0_pool_buffer:0',
    'StatefulPartitionedCall:17': 'call_state_block1_layer3_stream_buffer:0',
    'StatefulPartitionedCall:34': 'call_state_block3_layer0_pool_frame_count:0',
    'StatefulPartitionedCall:5': 'call_state_block0_layer1_stream_buffer:0',
    'StatefulPartitionedCall:20': 'call_state_block2_layer0_stream_buffer:0',
    'StatefulPartitionedCall:49': 'call_state_block3_layer5_stream_buffer:0',
    'StatefulPartitionedCall:64': 'call_state_block4_layer6_pool_buffer:0',
    'StatefulPartitionedCall:24': 'call_state_block2_layer2_pool_buffer:0',
    'StatefulPartitionedCall:66': 'call_state_head_pool_buffer:0',
    'StatefulPartitionedCall:53': 'call_state_block4_layer1_pool_buffer:0',
    'StatefulPartitionedCall:13': 'call_state_block1_layer2_pool_frame_count:0',
    'StatefulPartitionedCall:12': 'call_state_block1_layer2_pool_buffer:0',
    'StatefulPartitionedCall:18': 'call_state_block2_layer0_pool_buffer:0',
    'StatefulPartitionedCall:58': 'call_state_block4_layer3_pool_frame_count:0',
    'StatefulPartitionedCall:15': 'call_state_block1_layer3_pool_buffer:0',
    'StatefulPartitionedCall:45': 'call_state_block3_layer4_pool_buffer:0',
    'StatefulPartitionedCall:31': 'call_state_block2_layer4_pool_frame_count:0',
    'StatefulPartitionedCall:55': 'call_state_block4_layer2_pool_buffer:0',
    'StatefulPartitionedCall:48': 'call_state_block3_layer5_pool_frame_count:0',
    'StatefulPartitionedCall:28': 'call_state_block2_layer3_pool_frame_count:0',
    'StatefulPartitionedCall:47': 'call_state_block3_layer5_pool_buffer:0',
    'StatefulPartitionedCall:42': 'call_state_block3_layer3_pool_buffer:0',
    'StatefulPartitionedCall:22': 'call_state_block2_layer1_pool_frame_count:0',
    
    'StatefulPartitionedCall:0': 'logits', # probability
}


def image_standardize(img_array):
    standardized_img = (img_array - image_mean) / image_std
    return standardized_img

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
    # image = image_standardize(image)

    image = tf.expand_dims(image, axis=0)
    image = tf.expand_dims(image, axis=0)
    
    return image

def load_and_preprocess_video(file_paths, res):
    """Process each video using TensorFlow operations."""
    video = tf.map_fn(lambda x: tf_preprocess_image(x, res), file_paths, fn_output_signature=tf.float32)
    return video

def openvino_predict(compiled_model=None, mp4_file_path=None, jpg_folder_path=None, input_state=None, output_state=False, resolution=172):

    TFLite_model_path = "openvino/a2_float32.tflite"

    interpreter = tf.lite.Interpreter(model_path=TFLite_model_path, num_threads=8)
    runner = interpreter.get_signature_runner()
    input_details = runner.get_input_details()


    def quantized_scale(name, state):
        """Scales the named state tensor input for the quantized model."""
        dtype = input_details[name]['dtype']
        scale, zero_point = input_details[name]['quantization']
        # print(f"dtype: {dtype}, scale: {scale}, zero_point: {zero_point}")

        if 'frame_count' in name or dtype == np.float32 or scale == 0.0:
            return state

        # return np.cast((state / scale + zero_point), dtype)
        return (state / scale + zero_point).astype(dtype)

    
    def quantized_scale_cast(name, state):
        """Scales the named state tensor input for the quantized model."""
        dtype = input_details[name]['dtype']
        scale, zero_point = input_details[name]['quantization']
        # print(f"dtype: {dtype}, scale: {scale}, zero_point: {zero_point}")

        if 'frame_count' in name or dtype == np.float32 or scale == 0.0:
            return state

        return tf.cast((state / scale + zero_point), dtype)

    def rename_input(name):
        return "call_" + str(name) + ":0"

    def get_input_name(output_name):
        return output_to_input_map.get(output_name, None)

    init_states = {
        name: quantized_scale(name, np.zeros(x['shape'], dtype=x['dtype']))
        for name, x in input_details.items()
        if name != 'image'
    }

    # print(init_states)
    # print(len(init_states.keys()))


    if mp4_file_path is not None:
        mv_clip = VideoFileClip(mp4_file_path)
        mv_clip = mv_clip.resize((resolution,resolution))

        video = []
        clip = []

        for frame in mv_clip.iter_frames(fps=10):
            img = Image.fromarray(frame)
            img = img.resize((resolution, resolution))
            img_array = np.array(img, dtype=np.float32)
            img_array = img_array / 255.0

            # img_processed = image_standardize(img_array)

            img_processed = tf.expand_dims(img_array, axis=0)
            img_processed = tf.expand_dims(img_processed, axis=0)

            # print(img_processed.shape)
            # print(img_processed.dtype)

            video.append(img_processed)
            clip.append(img_array)

    elif jpg_folder_path is not None:

        wildcard_path = tf.strings.join([jpg_folder_path, '/*.jpg'])

        video_files = tf.io.matching_files(wildcard_path)

        video = load_and_preprocess_video(video_files, resolution)
        # print(len(video))
        


    """
    Start Predicting...
    """

    all_logits = []
    start = datetime.now()
    
    # current_states = {}
    current_states = init_states

    for frame in video:

        flatten_tensor = tf.reshape(frame, [-1])
        print(flatten_tensor[:10][:10]*255)


        # print(len(current_states.keys()))

        input_layer = compiled_model.input(0)
        output_layer = compiled_model.output(0)


        current_states['image'] = frame

        infer_request = compiled_model.create_infer_request()
        infer_request.infer(current_states)

        outputs = {}
        for output in compiled_model.outputs:
            output_name = output.get_any_name()
            outputs[output_name] = infer_request.get_tensor(output).data

        # print(outputs.keys())
        logits = outputs.pop('logits')[0]

        # print(outputs['state_block4_layer1_pool_buffer'])

        for key in outputs:
            current_states[key][:] = outputs[key]

        # current_states = outputs
        

        # probs = tf.nn.softmax(tf.cast(logits, dtype='float'))
        probs = tf.nn.softmax(tf.convert_to_tensor(logits, dtype='float32')).numpy()  # 確保 probs 是 NumPy 陣列

        # print(probs)

        # print(logits)
        all_logits.append(logits)


    end = datetime.now()

    print(f"Inference Time: {end-start}")
    

    
    # print(all_logits)
    print(logits) # [-40 -33 -29 -21 -58 -46 -29] -> max: -21
    probs = tf.nn.softmax(tf.cast(logits, dtype='float'))
    # print(probs)


    if mp4_file_path is not None:
        clip_np = tf.stack(clip).numpy()
        # print(clip_np.shape)
        if output_state:
            return probs, all_logits, clip_np, states
        return probs, all_logits, clip_np

    if jpg_folder_path is not None:
        return probs, all_logits