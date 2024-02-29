#搜索<div class="vice-list">
import re
import os
import requests

def extract_data_mp3_and_text(text):
    pattern = r'data-mp3="(.*?)">.*?<span>(.*?)</span>.*?</a>'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def download_audio(url, file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)  # 自动创建目录
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download: {url}")


# 指定文件路径
file_path = os.path.join(os.path.expanduser('~'), 'Desktop', '李信.txt')

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 提取data-mp3的值和文本内容
extracted_values = extract_data_mp3_and_text(text)

# 下载每个音频文件
for index, (audio_url, audio_text) in enumerate(extracted_values):
    audio_url = 'https:' + audio_url
    audio_file_name = os.path.join('C:\\Users\\24766\\Desktop\\李信', f'{audio_text}.mp3')
    download_audio(audio_url, audio_file_name)
