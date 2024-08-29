import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from PIL import Image
import cv2


label_map = ["0_Background","1_Entry","2_Bag_Operation","3_Machine_Operation","4_Item_Pickup","5_Normal_Scanning","6_Abnormal_Scanning_Skipping","7_Abnormal_Scanning_TwoAtATime","8_Abnormal_Scanning_CoverUp","9_Abnormal_Scanning_HidingBehind","10_Leaving"]
num_classes = len(label_map)
confusion_mat = np.loadtxt('evaluation/test_matrix_a2_V1.2_f0.864_acc0.848.txt', dtype=int)

row_sums = confusion_mat.sum(axis=1, keepdims=True)
confusion_mat = confusion_mat / row_sums

predicted_counts = confusion_mat.sum(axis=0)
actual_counts = confusion_mat.sum(axis=1)


print("Actual counts:", actual_counts)
print("Predicted counts:", predicted_counts)



print("Confusion Matrix:")
print(confusion_mat)

plt.figure(figsize=(18, 14))
plt.imshow(confusion_mat, cmap='Blues')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xlabel('Predicted',fontsize=14)
plt.ylabel('Actual',fontsize=14)
tick_marks = np.arange(num_classes)
plt.xticks(tick_marks, label_map, rotation=20)
plt.yticks(tick_marks, label_map)

for i in range(num_classes):
    for j in range(num_classes):
        if i==j:
            plt.text(j, i, round(confusion_mat[i, j], 2),
                    horizontalalignment='center',
                    verticalalignment='center',
                    color='black')
                    # color='white')
        else:
            plt.text(j, i, round(confusion_mat[i, j], 2),
                    horizontalalignment='center',
                    verticalalignment='center',
                    color='black')

plt.show()
plt.savefig('plots/confusion_matrix.png', format='png')
