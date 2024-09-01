import cv2
import subprocess

def reset_fps(video_path, out_fps, output_file_path):

    video_info(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{output_file_path[:-4]}_temp.mp4', fourcc, out_fps, (int(cap.get(3)), int(cap.get(4))))
    
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        i += 1

        if i % 3 == 0:
            out.write(frame)

    cap.release()
    out.release()
    subprocess.run(['ffmpeg', '-i',f'{output_file_path[:-4]}_temp.mp4',f'{output_file_path}'])

    video_info(output_file_path)



def video_info(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"FPS: {fps}")
    print(f"Frame: {frame_count}")
    print(f"Resolution: {height}x{width}")
    
    cap.release()

if __name__ == '__main__':
    reset_fps("raw_mp4/2024-07-03/2024-07-03-11-03-45#.mp4",10,"raw_mp4/reset_clips/aaa.mp4")