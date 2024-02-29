import os
from moviepy.editor import *

def convert_mp4_to_wav(source_path, target_path):
    video = VideoFileClip(source_path)
    audio = video.audio
    audio.write_audiofile(target_path)

def convert_folder_mp4_to_wav(input_folder, output_folder):
    # 确保输出文件夹存在，如果不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.mp4'):
            source_path = os.path.join(input_folder, file_name)
            target_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.wav')
            convert_mp4_to_wav(source_path, target_path)
            print(f"转换完成：{file_name}")

# 使用示例
input_folder = input("请输入源MP4文件所在的文件夹完整路径: ")
output_folder = input("请输入输出WAV文件的目标文件夹完整路径: ")
convert_folder_mp4_to_wav(input_folder, output_folder)
