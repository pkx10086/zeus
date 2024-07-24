import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def download_chunk(session, chunk_info, output_file):
    """
    下载文件的一个片段。

    使用提供的session对象，根据chunk_info中的起始和结束位置，从服务器请求并下载指定范围的文件数据。
    数据将被写入到output_file中。

    参数:
    - session: requests.Session对象，用于发起HTTP请求。
    - chunk_info: 元组，包含要下载的文件片段的起始和结束字节位置。
    - output_file: 字符串，表示正在下载的文件的路径。

    返回:
    无
    """
    # 解析chunk_info元组，获取片段的起始和结束字节位置
    start, end = chunk_info
    # 设置请求头，指定需要下载的字节范围
    headers = {'Range': f'bytes={start}-{end}'}
    try:
        # 发起GET请求，请求特定范围的文件数据
        response = session.get(url, headers=headers, stream=True)
        # 如果服务器返回的状态码是206（部分内容），则表示请求的文件片段已成功获取
        if response.status_code == 206:  # Partial Content
            # 打开输出文件，以读写模式进行操作
            with open(output_file, "r+b") as file:
                # 将文件指针定位到片段的起始位置
                file.seek(start)
                # 将获取到的片段数据写入到文件中
                file.write(response.content)
        else:
            # 如果服务器返回的状态码不是206，则打印错误信息
            print(f"Failed to download chunk {start}-{end}: status code {response.status_code}")
    except Exception as e:
        # 如果在下载过程中发生异常，则打印异常信息
        print(f"Error downloading chunk {start}-{end}: {e}")

def download_file_concurrently(url, output_file, num_threads=5):
    """
    并发下载一个文件。

    参数:
    url (str): 要下载文件的URL。
    output_file (str): 保存已下载文件的路径。
    num_threads (int, 可选): 用于并发下载的线程数。默认为5。

    返回:
    None
    """
    # 初始化HTTP请求会话
    session = requests.Session()
    # 发送HEAD请求以获取文件大小
    response = session.head(url)
    # 获取文件的总大小
    total_size = int(response.headers['Content-Length'])

    # 检查文件是否已经存在并且大小是否完整
    if os.path.exists(output_file):
        local_size = os.path.getsize(output_file)
        if local_size >= total_size:
            print("\n文件已经下载完成。")
            return

    # 计算每个分片的大小以供并发下载
    chunk_size = total_size // num_threads
    # 将文件分割成分片
    chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads)]
    # 调整最后一个分片的大小以确保所有字节都被下载
    chunks[-1] = (chunks[-1][0], total_size - 1)

    # 以二进制写模式打开输出文件，并将其截断至文件的总大小
    with open(output_file, "wb") as file:
        file.truncate(total_size)

    # 使用ThreadPoolExecutor进行并发下载文件分片
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交每个分片的下载任务
        futures = [executor.submit(download_chunk, session, chunk, output_file) for chunk in chunks]

        # 监控每个下载任务的进度
        for future in tqdm(as_completed(futures), total=len(chunks), unit='分片'):
            try:
                future.result()
            except Exception as e:
                # 打印下载过程中发生的任何异常
                print(f"处理分片时发生错误: {e}")
# 使用示例
url = "https://example.com/largefile.zip"
output_file = "largefile.zip"


if __name__ == '__main__':
    #url = 'https://cm11-c110-3.play.bokecc.com/flvs/ca/QxZra/66Nh7jNz8c-90.mp4?t=1721813556&key=9D9ADEB5318E9F508AC55ED1EF6A1BA1&tpl=10'
    #filename = '66Nh7jNz8c-90.mp4'
    print('*' * 100)
    print('\t\t\t欢迎使用文件下载小助手')
    print('作者:panKx date:2024-07-24')
    print('*' * 100)
    url = input('请输入需要下载的文件链接:\n')
    output_file = input('请输入需要输出的文件名:\n')
    download_file_concurrently(url, output_file)