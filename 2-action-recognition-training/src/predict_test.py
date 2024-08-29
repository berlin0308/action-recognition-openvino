import numpy as np
import os
import tensorflow as tf
import progressbar
from sklearn.metrics import classification_report, confusion_matrix,f1_score, accuracy_score

from predict import predict_behavior

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

image_mean = np.array([0.40742482, 0.41668848, 0.39488508], dtype=np.float32)
image_std = np.array([0.2889984, 0.28819978, 0.28711625], dtype=np.float32)

def image_standardize(img_array):
    standardized_img = (img_array - image_mean) / image_std
    return standardized_img.astype(np.float32)

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=-1, keepdims=True)


saved_model_dir = f'results/a2_b8_lr0.000545_g2.5_d0.6_sd0.2_86/savedmodel'
test_data_root = "data/V1.2/test"
num_frames = 16
model_id = 'a2'

resolution = 172
if model_id == "a2":
    resolution = 224


label_map = ["0_Background","1_Entry","2_Bag_Operation","3_Machine_Operation","4_Item_Pickup","5_Normal_Scanning","6_Abnormal_Scanning_Skipping","7_Abnormal_Scanning_TwoAtATime","8_Abnormal_Scanning_CoverUp","9_Abnormal_Scanning_HidingBehind","10_Leaving"]

y_trues = []
y_preds = []
y_probs = []

best_thresholds = []

calibrated = False


saved_model = tf.saved_model.load(saved_model_dir)

init_states_fn = saved_model.signatures['init_states']
saved_model = saved_model.signatures['call']

input_shape = tf.constant([1, 1, resolution, resolution, 3])
init_states = init_states_fn(input_shape)



print("Loading...")
progress = progressbar.ProgressBar(maxval=700)
progress.start()

state = init_states.copy()

t = 0
for i, class_name in enumerate(label_map):


    class_root = os.path.join(test_data_root, class_name)
    print("\n"+class_root)


    for j, clip_name in enumerate(sorted(os.listdir(class_root),key=str)):

        # if j > 5:
        #     break

        jpg_folder_path = os.path.join(class_root, clip_name)
        print("\n"+jpg_folder_path)

            
        y_true = i

        probs, all_logits = predict_behavior(runner=None, resolution=resolution, jpg_folder_path=jpg_folder_path
                                                                , input_state=state, output_state=False, saved_model=saved_model)
        y_pred = int(np.argmax(probs))


        print(f"True Label: {y_true}, Predicted: {y_pred}")
        y_trues.append(y_true)
        y_preds.append(y_pred)

        y_probs.append(probs.numpy().tolist())
        # print(y_probs)
        # print(y_trues)

        print('\n')

        t += 1
        progress.update(t)


progress.finish()



print(classification_report(y_trues, y_preds))
print(confusion_matrix(y_trues, y_preds))

f1 = round(f1_score(y_trues, y_preds, average='macro'), 3)
accuracy = round(accuracy_score(y_trues, y_preds), 3)
print(f'\nF1-score: {f1} \nAccuracy:{accuracy}')
