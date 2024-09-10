import cv2
import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips

def extract_frames(video_path, output_dir):
    # Clear the output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f'Extracted {frame_count} frames to {output_dir}')

def run_gfpgan_inference(input_dir, output_dir):
    # Clear the enhanced frames directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Run the GFPGAN inference
    os.system(f'python inference_gfpgan.py -i {input_dir} -o {output_dir} -v 1.4 -s 2')

def create_video_from_frames(input_dir, output_video_path):
    # Directory to save the output video
    output_dir = os.path.dirname(output_video_path)
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all frame filenames in the input directory
    frame_filenames = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])

    # Read the first frame to get the dimensions
    first_frame = cv2.imread(os.path.join(input_dir, frame_filenames[0]))
    height, width, layers = first_frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID', 'MJPG', etc.
    video = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))

    # Write each frame to the video
    for frame_filename in frame_filenames:
        frame = cv2.imread(os.path.join(input_dir, frame_filename))
        video.write(frame)

    # Release the VideoWriter object
    video.release()
    print(f'Video saved to {output_video_path}')

def add_audio_to_video(original_video_path, video_without_audio_path, final_output_path):
    # Load the original video and extract the audio
    original_video = VideoFileClip(original_video_path)
    audio = original_video.audio

    # Check if the original video has audio
    if audio is None:
        print("Error: The original video does not contain any audio.")
        return

    # Load the video without audio
    video = VideoFileClip(video_without_audio_path)

    # Set the audio of the video
    final_video = video.set_audio(audio)

    # Write the final video to file
    final_video.write_videofile(final_output_path, codec='libx264', audio_codec='aac')
    print(f'Final video with audio saved to {final_output_path}')

if __name__ == "__main__":
    video_path = 'inputs/input.mp4'
    frames_dir = 'frames'
    enhanced_frames_dir = 'enhanced_frames/restored_imgs'
    final_output_video_path = 'outputs/enhanced_video.mp4'

    # Step 1: Extract frames from the video
    extract_frames(video_path, frames_dir)

    # Step 2: Run GFPGAN inference to enhance frames
    run_gfpgan_inference(frames_dir, 'enhanced_frames')

    # Step 3: Create a video from the enhanced frames
    temp_output_video_path = 'outputs/temp_enhanced_video.mp4'
    create_video_from_frames(enhanced_frames_dir, temp_output_video_path)

    # Step 4: Add audio to the final video and save it
    add_audio_to_video(video_path, temp_output_video_path, final_output_video_path)

    # Step 5: Remove the temporary video file
    os.remove(temp_output_video_path)