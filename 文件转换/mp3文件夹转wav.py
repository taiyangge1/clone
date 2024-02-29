import os
from pydub import AudioSegment

# 指定桌面上的文件夹路径
folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "新建文件夹")  # 请替换"your_folder"为您的文件夹名
output_file = "combined.wav"  # 合并后的文件名

# 读取所有WAV文件
wav_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# 合并WAV文件
combined = AudioSegment.empty()
for wav_file in wav_files:
    path_to_wav = os.path.join(folder_path, wav_file)
    sound = AudioSegment.from_wav(path_to_wav)
    combined += sound

# 导出为WAV格式
combined.export(os.path.join(folder_path, output_file), format="wav")

print("合并完成，文件保存在：", os.path.join(folder_path, output_file))
