import cv2
import os
import shutil
import argparse

'''
source venv/bin/activate
'''

def save_clip(video_path, start_time, output_file):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    start_frame = int(max(0, start_time * fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    
    i = 0
    while i < 16:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        i += 1

    cap.release()
    out.release()
    print(f"Saved clip: {start_time:.2f}")

def play_saved_clip(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("play_saved_clip Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    print(f"Number of frames: {total_frames}")
    print(f"Duration: {duration:.2f} seconds")

    new_window_name = f"Playback - {os.path.basename(video_path)}"
    cv2.namedWindow(new_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(new_window_name, 640, 480)

    # Play the video in the new window
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # hard display TODO need modify
        cv2.putText(frame, '0_Background'
                    , (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '1_Entry'
                    , (600, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '2_Bag_Operation'
                    , (600, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '3_Machine_Operation'
                    , (600, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '4_Item_Pickup'
                    , (600, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '5_Normal_Scanning'
                    , (600, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.putText(frame, '6_Abnormal_Scanning_Skipping'
                    , (600, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '7_Abnormal_Scanning_TwoAtATime'
                    , (600, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '8_Abnormal_Scanning_CoverUp'
                    , (600, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '9_Abnormal_Scanning_HidingBehind'
                    , (600, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, '10_Leaving'
                    , (600, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow(new_window_name, frame)
        if cv2.waitKey(int(1000/fps)) & 0xFF == 27:  # ESC key to exit
            break
    

    # class_id = input("Enter class ID (0-6): ")
    class_map = {
        "0": "0_Background",
        "1": "1_Entry",
        "2": "2_Bag_Operation",
        "3": "3_Machine_Operation",
        "4": "4_Item_Pickup",
        "5": "5_Normal_Scanning",
        "6": "6_Abnormal_Scanning_Skipping",
        "7": "7_Abnormal_Scanning_TwoAtATime",
        "8": "8_Abnormal_Scanning_CoverUp",
        "9": "9_Abnormal_Scanning_HidingBehind",
        "10": "10_Leaving",
    }

    key = cv2.waitKey(0)

    if int(key) >= 48:
        class_id = str(int(key)-48) # 1, 2, ..., 9
    else:
        class_id = str(int(key)+7) # F1, F2, F3 -> 11, 12, 13
    
    if class_id == '20':
        class_id = '10' # F10 -> 10

    print(f"Class: {class_id}")

    
    if class_id in class_map:
        destination_folder = os.path.join('labeled_mp4', class_map[class_id])
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.copy(video_path, os.path.join(destination_folder, os.path.basename(video_path)))
        print(f"Video copied to {destination_folder}.")

    cap.release()
    cv2.destroyAllWindows()

def frame_saver(video_path=None):

    clip_name = video_path.split('\\')[-1].split('.')[0]
    labeled_save_path = 'temp_mp4'

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")
    delay = int(1000 / fps)
    
    # Read the first frame and display it
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return
    cv2.imshow('Video', frame)
    
    playing = True
    current_frame_count = 0
    while True:
        # print(f"Current frame: {current_frame_count}")

        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count)
        ret, frame = cap.read()
        cv2.putText(frame, f'Frame: {current_frame_count} ({current_frame_count/10} sec)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if ret:
            cv2.imshow('Video', frame)


        if playing:
            current_frame_count += 1

        key = cv2.waitKeyEx(1)

        if key == ord(' '):  # Space bar to toggle play/pause
            playing = not playing
            if playing:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Video', frame)
                if cv2.waitKey(delay) == ord(' '):
                    playing = False

        elif key == 63234:  # Left arrow key to rewind 5 seconds
            current_frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES) - 5 * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame_count))
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video', frame)

        elif key == 63235:  # Right arrow key to skip 5 seconds
            current_frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES) + 5 * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, min(cap.get(cv2.CAP_PROP_FRAME_COUNT), current_frame_count))
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Video', frame)

        elif key == ord('s'):  # 's' to save the clip
            current_frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)
            start_time = max(0, (current_frame_count / fps) - 1.6)

            #output_file_path = f'{labeled_save_path}/{clip_name}_{int(current_frame_count)}.mp4'
            output_file_path = os.path.join(labeled_save_path, f'{clip_name}_{int(current_frame_count)}.mp4')
            save_clip(video_path, start_time, output_file_path)
            play_saved_clip(output_file_path)

        elif key == 27:  # ESC key to exit
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process video frames from a given video file.')
    parser.add_argument('video_path', type=str, help='Path to the video file')

    args = parser.parse_args()

    frame_saver(video_path=args.video_path)
