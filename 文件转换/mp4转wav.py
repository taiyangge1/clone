import os
from moviepy.editor import *

def convert_mp4_to_wav(full_file_name):
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    source_path = os.path.join(desktop, full_file_name)
    target_path = os.path.join(desktop, os.path.splitext(full_file_name)[0] + '.wav')

    video = VideoFileClip(source_path)
    audio = video.audio
    audio.write_audiofile(target_path)

# 使用示例
# 请确保输入完整的文件名，例如 'video.mp4'
file_name = input("请输入视频完整名称（包括扩展名）: ")
convert_mp4_to_wav(file_name)
