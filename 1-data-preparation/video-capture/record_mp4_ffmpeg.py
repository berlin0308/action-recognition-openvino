import cv2
import datetime
import os
import json
import win32api
import win32con
import ffmpeg
import numpy as np

def set_english_input():
    hkl = win32api.LoadKeyboardLayout('00000409', win32con.KLF_ACTIVATE)
    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_INPUTLANGCHANGEREQUEST, 0, hkl)

class_names = ['0_Normal', '1_Skipping', '2_TwoAtATime', '3_ItemStacking', '4_PretendScanning', '5_HidingBehind']
saved_filename = None

x_start, y_start, x_end, y_end = 0, 0, 0, 0


TARGET_FPS = 10.0
SAVE_CROP = True
SAVE_RAW = True

def update_region(config_path, new_x1, new_y1, new_x2, new_y2):
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    config['x1'] = new_x1
    config['y1'] = new_y1
    config['x2'] = new_x2
    config['y2'] = new_y2

    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)
    
    print(f"Config updated: {config}")

def draw_scale(frame, step=100):
    height, width = frame.shape[:2]
    for x in range(0, width, step):
        cv2.line(frame, (x, 0), (x, 10), (255, 255, 255), 1)
        cv2.putText(frame, str(x), (x, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    for y in range(0, height, step):
        cv2.line(frame, (0, y), (10, y), (255, 255, 255), 1)
        cv2.putText(frame, str(y), (20, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

def play_video(filename):
    cap = cv2.VideoCapture(filename)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    if not cap.isOpened():
        print(f"Error: Could not open video {filename}.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Playback', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def set_region(event, x, y, flags, params):
    global x_start, y_start, x_end, y_end
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x, y
        x_end, y_end = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        x_end, y_end = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        update_region(config_path, x_start, y_start, x_end, y_end)

def record_video(x1, y1, x2, y2, rtsp_url):
    global x_start, y_start, x_end, y_end
    x_start, y_start, x_end, y_end = x1, y1, x2, y2

    probe = ffmpeg.probe(rtsp_url)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    print(f"W: {width}, H: {height}")

    out = (
        ffmpeg
            .input(rtsp_url, rtsp_transport='tcp')
            .output('pipe:', format='rawvideo', pix_fmt='bgr24', loglevel="quiet", r=25)
            .run_async(pipe_stdout=True)
    )

    recording = False
    i = 0
    cnt_empty = 0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    crop_out = None

    while True:
        in_bytes = out.stdout.read(height * width * 3)
        if not in_bytes:
            cnt_empty += 1
            if cnt_empty > 10:
                break
        cnt_empty = 0
        frame = np.frombuffer(in_bytes, dtype=np.uint8).reshape(height, width, 3)

        frame = cv2.flip(frame, 1)
        i += 1

        if i % 3 == 0:
            raw_frame = frame.copy()
            draw_scale(frame)
            cv2.rectangle(frame, (x_start-2, y_start-2), (x_end+2, y_end+2), (0, 255, 0), 2)
            
            if recording:
                cropped_frame = frame[y_start:y_end, x_start:x_end]
                if crop_out is None:
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                    save_folder = f"collected_mp4/{current_date}"
                    if not os.path.exists(save_folder):
                        os.makedirs(save_folder, exist_ok=True)
                    filename = f"{save_folder}/{current_time}.mp4"
                    crop_out = cv2.VideoWriter(filename, fourcc, TARGET_FPS, (x_end - x_start, y_end - y_start))
                    raw_out = cv2.VideoWriter(f"{filename[:-4]}_raw.mp4", fourcc, TARGET_FPS, (width, height))



                if SAVE_CROP:
                    crop_out.write(cropped_frame)
                if SAVE_RAW:
                    raw_out.write(raw_frame)

                cv2.putText(frame, "RECORDING...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.putText(frame, str(int(i / 30)), (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            cv2.setMouseCallback('frame', set_region)

            key = cv2.waitKey(1)
            if key == ord('r') or key == ord('R') or key == ord(' '):
                if recording:
                    recording = False
                    if SAVE_CROP:
                        crop_out.release()
                        crop_out = None
                    if SAVE_RAW:
                        raw_out.release()
                        raw_out = None
                    print(f"Recording stopped. Video saved as {filename}.")
                    saved_filename = filename
                else:
                    recording = True
                    print("Recording started.")

            elif key == ord('v') and saved_filename:
                play_video(saved_filename)
            elif key == ord('q'):
                break
        
    if out is not None:
        out.release()
    if raw_out is not None:
        raw_out.release()
    cv2.destroyAllWindows()

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

if __name__ == "__main__":
    config_path = 'config.json'
    config = load_config(config_path)
    x1, y1, x2, y2 = config['x1'], config['y1'], config['x2'], config['y2']
    rtsp_url = config['rtsp_url']
    set_english_input()

    record_video(x1, y1, x2, y2, rtsp_url)
