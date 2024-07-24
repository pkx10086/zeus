#-*- coding: UTF-8 -*-
import requests
from contextlib import closing

class ProgressBar(object):
    """
   进度条类的初始化方法。

   该类用于创建和管理一个表示进度的进度条。

   参数:
       title(str): 进度条的标题。
       count(float): 当前进度的值，默认为0.0。
       run_status(str): 运行状态的字符串，默认为None。如果未提供，则默认为空字符串。
       fin_status(str): 完成状态的字符串，默认为None。如果未提供，则默认为空格数量与run_status相同的字符串。
       total(float): 进度条的总长度，默认为100.0。
       unit(str): 进度单位，默认为空字符串。
       sep(str): 进度和状态之间的分隔符，默认为'/'。
       chunk_size(float): 每个进度块的大小，默认为1.0。
   """
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        #[名称] 状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count = 1, status = None):
        self.count += count
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str, )


if __name__ == '__main__':
    #url = 'https://cm11-c110-3.play.bokecc.com/flvs/ca/QxZra/66Nh7jNz8c-90.mp4?t=1721813556&key=9D9ADEB5318E9F508AC55ED1EF6A1BA1&tpl=10'
    #filename = '66Nh7jNz8c-90.mp4'
    print('*' * 100)
    print('\t\t\t欢迎使用文件下载小助手')
    print('作者:panKx date:2024-07-24')
    print('*' * 100)
    url  = input('请输入需要下载的文件链接:\n')
    filename = url.split('/')[-1]
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print('文件大小:%0.2f KB' % (content_size / chunk_size))
            progress = ProgressBar("%s下载进度" % filename
                                   , total = content_size
                                   , unit = "KB"
                                   , chunk_size = chunk_size
                                   , run_status = "正在下载"
                                   , fin_status = "下载完成")
            # 去掉url中的参数,有一些文件后面是加密的带参数，需要去掉参数
            filename = filename.split('?')[0]
            with open(filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        else:
            print('链接异常')