import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error: {e}"

def get_name(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        # 查找包含 'vod_name' 和 'vod_part' 的 script 标签
        script_tags = soup.find_all('script')
        for script in script_tags:
            if 'vod_name' in script.text and 'vod_part' in script.text:
                # 使用正则表达式提取信息
                vod_name_match = re.search(r"var vod_name = '(.*?)'", script.text)
                vod_part_match = re.search(r"vod_part='(.*?)'", script.text)

                if vod_name_match and vod_part_match:
                    vod_name = vod_name_match.group(1)
                    vod_part = vod_part_match.group(1)
                    name=vod_name+vod_part+".mp4"
                    return name
    except requests.RequestException as e:
        return f"Error: {e}"

def extract_video_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script')
    for script in script_tags:
        if 'config' in script.text:
            start = script.text.find('"url": "') + 8  # 加 8 是为了跳过 "url": "
            end = script.text.find('",', start)
            video_url = script.text[start:end]
            return video_url
    return None

def download_video(url, filename):
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            logging.error("ERROR, something went wrong")
        else:
            print(f"Video downloaded successfully: {filename}")
    except requests.RequestException as e:
        logging.error(f"Error: {e}")

# 主程序
def main():
    base_url = "https://www.ddcomic.com/addons/dp/player/dp.php?key=0&from=yhdm&id=&api=&url="
    input_url = input("请输入视频页面的url地址: ")
    download_directory = "E:\番剧\樱花动漫\《欢迎来到实力至上主义教室第二季》"
    full_url = base_url + input_url

    name = get_name(input_url)
    html_content = get_html(full_url)
    if html_content.startswith("Error"):
        print(html_content)
    else:
        video_url = extract_video_url(html_content)
        if video_url:
            video_filename = os.path.join(download_directory, name)  # 将文件名和下载目录合并
            logging.info(f"正在为您下载到指定目录: {video_filename}")
            download_video(video_url, video_filename)
        else:
            logging.error("无法找到视频下载链接")

if __name__ == "__main__":
    main()