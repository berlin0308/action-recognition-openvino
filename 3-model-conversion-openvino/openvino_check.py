from openvino.runtime import Core, serialize
from openvino.tools.ovc import convert_model
import openvino.runtime as ov
import tensorflow as tf
import numpy as np
from openvino_predict import openvino_predict
import os
import sys
from sklearn.metrics import classification_report, confusion_matrix,f1_score, accuracy_score


label_map = ["0_Background","1_Entry","2_Bag_Operation","3_Machine_Operation","4_Item_Pickup","5_Normal_Scanning","6_Abnormal_Scanning_Skipping","7_Abnormal_Scanning_TwoAtATime","8_Abnormal_Scanning_CoverUp","9_Abnormal_Scanning_HidingBehind","10_Leaving"]

def get_top_k(probs, k=3):

  # print(label_map)
  """Outputs the top k model labels and probabilities on the given video."""
  top_predictions = tf.argsort(probs, axis=-1, direction='DESCENDING')[:k]
  top_labels = tf.gather(label_map, top_predictions, axis=-1)
  top_labels = [label.decode('utf8') for label in top_labels.numpy()]
  top_probs = tf.gather(probs, top_predictions, axis=-1).numpy()
  return tuple(zip(top_labels, top_probs))



output_model_path = 'openvino/movinet_a2_fp16_model.xml'

core = Core()
compiled_model = core.compile_model(model=output_model_path, device_name="CPU")


# mp4_file_path = "data/Dataset_DA/1209_O/NL/20231209-00-02-03.mp4"
# mp4_file_path = "data/Dataset_DA/1211_O/DR/20231211-04-17-03.mp4"
# mp4_file_path = "data/Dataset_DA/1216_O/FD/20231216-00-06-04.mp4"
# mp4_file_path = "data/Dataset_DA/1216_O/RM/20231216-01-52-03.mp4"
mp4_file_path = "openvino/aaa.mp4"
probs, all_logits, clip_np = openvino_predict(compiled_model=compiled_model, mp4_file_path=mp4_file_path, resolution=224)
top_k = get_top_k(probs, k=3)
print()
for label, prob in top_k:
  print(label, prob)


jpg_folder_path = "data/V1.2/V1.2_Preprocessed_jpgs/0_Background/2024-06-26-13-25-43_97"
probs, all_logits = openvino_predict(compiled_model=compiled_model, jpg_folder_path=jpg_folder_path, resolution=224)

# probs = tf.nn.softmax(logits)
top_k = get_top_k(probs, k=3)
print()
for label, prob in top_k:
  print(label, prob)


y_trues = []
y_preds = []
y_probs = []

day_label_root = "data/V1.2/V1.2_Preprocessed_jpgs"

for i, class_name in enumerate(label_map):

    if class_name == 'X':
        break

    class_root = os.path.join(day_label_root, class_name)
    print("\n"+class_root)

    if class_root.split('/')[-1][0] == '.':
        continue


    for j, clip_name in enumerate(sorted(os.listdir(class_root),key=str)):

        if j > 5:
            break

        jpg_folder_path = os.path.join(class_root, clip_name)
        print("\n"+jpg_folder_path)

            
        y_true = i

        probs, all_logits = openvino_predict(compiled_model=compiled_model, jpg_folder_path=jpg_folder_path, resolution=224)

        y_pred = int(np.argmax(probs))


        print(f"True Label: {y_true}, Predicted: {y_pred}")
        y_trues.append(y_true)
        y_preds.append(y_pred)

        y_probs.append(probs.numpy().tolist())
        # print(y_probs)
        # print(y_trues)





print(classification_report(y_trues, y_preds))
print(confusion_matrix(y_trues, y_preds))

f1 = round(f1_score(y_trues, y_preds, average='macro'), 3)
accuracy = round(accuracy_score(y_trues, y_preds), 3)
print(f'\nF1-score: {f1} \nAccuracy:{accuracy}')