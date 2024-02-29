import os
from pydub import AudioSegment

def find_mp3_files(directory):
    mp3_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))
    return mp3_files

def merge_mp3_files(mp3_files, output_filename):
    combined = AudioSegment.empty()
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio
    combined.export(output_filename, format="mp3")

def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

def main():
    folder_name = input("Enter the name of the folder on your Desktop: ")
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, folder_name)

    if os.path.exists(target_folder):
        mp3_files = find_mp3_files(target_folder)
        if mp3_files:
            combined_mp3 = os.path.join(target_folder, "combined_audio.mp3")
            combined_wav = os.path.join(target_folder, "combined_audio.wav")

            merge_mp3_files(mp3_files, combined_mp3)
            print(f"Combined MP3 file created at {combined_mp3}")

            convert_mp3_to_wav(combined_mp3, combined_wav)
            print(f"Converted WAV file created at {combined_wav}")
        else:
            print("No MP3 files found in the specified folder.")
    else:
        print("The specified folder does not exist on your Desktop.")

if __name__ == "__main__":
    main()
