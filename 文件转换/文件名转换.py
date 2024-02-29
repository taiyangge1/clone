import os

def rename_files_sequentially(directory):
    # 初始化文件序号
    file_number = 0

    for filename in os.listdir(directory):
        # 获取完整的文件路径
        file_path = os.path.join(directory, filename)

        # 检查是否是文件而不是目录
        if os.path.isfile(file_path):
            # 分离文件名和扩展名
            _, extension = os.path.splitext(filename)
            # 构建新的文件名，保持原有扩展名
            new_filename = f"{file_number}{extension}"
            # 重命名文件
            os.rename(file_path, os.path.join(directory, new_filename))
            print(f"Renamed '{filename}' to '{new_filename}'")

            # 更新文件序号
            file_number += 1

# 指定您的文件夹路径
folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', '李信')
rename_files_sequentially(folder_path)
