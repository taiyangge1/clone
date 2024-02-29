import os
import subprocess

def convert_to_mp4(source_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(".avi"):
                avi_file_path = os.path.join(root, file)
                mp4_file_path = os.path.join(target_path, os.path.splitext(file)[0] + '.mp4')
                subprocess.run(['ffmpeg', '-i', avi_file_path, mp4_file_path])

source_path = 'D:\BaiduNetdiskDownload\openpose'  # 把这里替换成你的.avi文件所在的路径
target_path = 'D:\BaiduNetdiskDownload\openpose'      # 把这里替换成你想存放mp4文件的路径

convert_to_mp4(source_path, target_path)
