from moviepy.editor import AudioFileClip

def convert_m4a_to_wav(input_file, output_file):
    audio_clip = AudioFileClip(input_file)
    audio_clip.write_audiofile(output_file, codec='pcm_s16le')

# 使用方法
input_m4a = 'C:\\Users\\24766\\Desktop\\1.m4a'  # 这里替换为你的 M4A 文件路径
output_wav = 'C:\\Users\\24766\\Desktop\\output.wav'  # 输出 WAV 文件的路径
convert_m4a_to_wav(input_m4a, output_wav)
