from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

# 指定包含视频的文件夹
folder_path = 'D:/进击的巨人素材/三笠/'  # 替换为你的文件夹路径

# 获取文件夹中所有的MP4文件
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp4')]

# 按文件名排序
files.sort()

# 读取视频文件
clips = [VideoFileClip(f) for f in files]

# 合并视频
final_clip = concatenate_videoclips(clips)

# 输出合并后的视频文件到指定位置
final_clip.write_videofile("D:/进击的巨人素材/三笠/combined_video.mp4")

# 将所有视频文件的名字写入一个文本文件
with open("D:/进击的巨人素材/三笠/combined_video_files.txt", "w") as file:
    for filename in files:
        file.write(os.path.basename(filename) + "\n")
