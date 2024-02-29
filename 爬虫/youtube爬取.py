import requests

# 设置视频的下载地址
url = 'https://rr3---sn-ogul7n7s.googlevideo.com/videoplayback?expire=1704133557\u0026ei=VK-SZfaHPM2W1d8P-KKWgAY\u0026ip=172.234.87.44\u0026id=o-AJkyS_z-yMHmgvAJKyM6yxmsnGXg43gNBp6ZkuBhsgSj\u0026itag=18\u0026source=youtube\u0026requiressl=yes\u0026xpc=EgVo2aDSNQ%3D%3D\u0026mh=EH\u0026mm=31%2C29\u0026mn=sn-ogul7n7s%2Csn-oguelnzs\u0026ms=au%2Crdu\u0026mv=m\u0026mvi=3\u0026pl=24\u0026initcwndbps=277500\u0026siu=1\u0026spc=UWF9fxa8CLt0LroTfW30GotXZYCzaj28cjje36JXEx9nFhsCnGnpoys\u0026vprv=1\u0026svpuc=1\u0026mime=video%2Fmp4\u0026ns=q0WIqYOgKMJvJK55EiOuyAkQ\u0026cnr=14\u0026ratebypass=yes\u0026dur=995.973\u0026lmt=1697100677012776\u0026mt=1704111680\u0026fvip=5\u0026fexp=24007246\u0026beids=24350017\u0026c=WEB\u0026txp=5538434\u0026n=DlTbC4teAdiX1dJ\u0026sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Csiu%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Ccnr%2Cratebypass%2Cdur%2Clmt\u0026sig=AJfQdSswRgIhAPWVTlSO_056PTa6czulp4DiHZ2DXf-1oTxQGfoDy20BAiEA7EnO3_b0w6VKjYzTRbQF4XPKsPTcKhkeOu-Enfjvd1E%3D\u0026lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps\u0026lsig=AAO5W4owRQIhAIsvS3-cnk87ADUjy9_nvNfxx5e6qDdBf6seB96t6C3RAiAHm148ACVyynmHeopievro8aVVmbpWQ-4ZZoYKSYinOQ%3D%3D'

# 设置请求头，有些网站可能需要特定的请求头来模拟浏览器行为
headers = {
    "authority": "www.youtube.com",
    "method": "GET",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "Sec-Ch-Ua-Arch": "\"x86\"",
    "Sec-Ch-Ua-Bitness": "\"64\"",
    "Sec-Ch-Ua-Full-Version": "\"120.0.6099.130\"",
    "Sec-Ch-Ua-Full-Version-List": "\"Not_A Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"120.0.6099.130\", \"Google Chrome\";v=\"120.0.6099.130\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": "\"\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Platform-Version": "\"15.0.0\"",
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Service-Worker-Navigation-Preload": "true",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 确保请求成功
if response.status_code == 200:
    # 设置文件名，你可以根据需要更改
    filename = 'downloaded_video.mp4'

    # 打开文件以便写入
    with open(filename, 'wb') as file:
        file.write(response.content)

    print('视频下载完成:', filename)
else:
    print('下载失败，状态码:', response.status_code)
