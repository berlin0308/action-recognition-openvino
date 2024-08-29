import os
import random
import shutil

def split_folder(input_folder, train_folder, test_folder):

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    
    sub_folders = ["0_Background","1_Entry","2_Bag_Operation","3_Machine_Operation","4_Item_Pickup","5_Normal_Scanning","6_Abnormal_Scanning_Skipping","7_Abnormal_Scanning_TwoAtATime","8_Abnormal_Scanning_CoverUp","9_Abnormal_Scanning_HidingBehind","10_Leaving"]
    print(sub_folders)
    train_samples = [30, 40, 120, 70, 90, 120, 75, 75, 55, 60, 50]
    
    for i, sub_folder in enumerate(sub_folders):

        current_sub_folder_path = os.path.join(input_folder, sub_folder)
        
        os.makedirs(os.path.join(train_folder, sub_folder), exist_ok=True)
        os.makedirs(os.path.join(test_folder, sub_folder), exist_ok=True)
        
        
        print(f"All data: {len(os.listdir(current_sub_folder_path))}")

        train_sample = train_samples[i]    
        print(f"train sample data: {train_sample}")

        # randomly select folders
        selected_folders = random.sample(os.listdir(current_sub_folder_path), train_sample)


        for folder_name in os.listdir(current_sub_folder_path):
            source_folder = os.path.join(current_sub_folder_path, folder_name)
            
            if folder_name in selected_folders:
                destination_folder = os.path.join(os.path.join(train_folder, sub_folder), folder_name)
                shutil.copytree(source_folder, destination_folder)
                print(source_folder)
                print(destination_folder)
            else:
                destination_folder = os.path.join(os.path.join(test_folder, sub_folder), folder_name)
                shutil.copytree(source_folder, destination_folder)
                print(source_folder)
                print(destination_folder)



            


if __name__ == '__main__':

    split_folder(input_folder='data/V1.2/V1.2_jpgs', train_folder='data/V1.2/train_test', test_folder='data/V1.2/test_test')
