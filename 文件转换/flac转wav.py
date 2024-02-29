from pydub import AudioSegment

def convert_flac_to_wav(input_file, output_file):
    try:
        audio = AudioSegment.from_file(input_file, format='flac')
        audio.export(output_file, format='wav')
        print(f"Converted {input_file} to {output_file}.")
    except Exception as e:
        print(f"Error converting {input_file} to WAV: {str(e)}")

if __name__ == "__main__":
    input_file = "C:\\Users\\24766\\Desktop\\3.wav_0key_sxc.flac"  # 输入的FLAC文件路径
    output_file = "C:\\Users\\24766\\Desktop\\3.wav_0key_sxc.wav"  # 输出的WAV文件路径

    convert_flac_to_wav(input_file, output_file)
