from pydub import AudioSegment
import os

# 指定桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 指定要转换的文件名
file_name = "1.wav"  # 将 'your_file.wav' 替换为你的文件名

# 完整的文件路径
wav_file_path = os.path.join(desktop_path, file_name)

# 检查文件是否存在
if os.path.exists(wav_file_path):
    # 读取.wav文件
    audio = AudioSegment.from_wav(wav_file_path)

    # 定义转换后的文件路径
    mp3_file_path = wav_file_path.replace(".wav", ".mp3")

    # 导出为.mp3格式
    audio.export(mp3_file_path, format="mp3")
    print(f"文件 {file_name} 已转换为 MP3.")
else:
    print(f"文件 {file_name} 不存在于桌面上.")
