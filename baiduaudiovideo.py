import base64
import urllib
import requests
import json
import os

success = open("success.txt", mode='w', encoding='utf8')


class AudioToText:
    ''' 利用 FFmpeg 提取视频中的语音并转换为文本文档'''

    def __init__(self):
        self.access_token = self.get_access_token()
        self.fmt = "pcm"

    def getFmt(self):
        return self.fmt;

    def get_path_files(self, path, type='.pcm'):
        '''
        获取目录下所有的 pcm文件
        :param path: 目录地址
        :param type: 文件类型
        :return: 包含文件路径的列表
        '''
        files = os.listdir(path)
        new = []
        for i in files:
            name, ty = os.path.splitext(i)
            if ty == type:
                pathFile = os.path.join(path, i)
                new.append(pathFile)
        return new

    def get_file_content(self, filePath):
        '''
        文件读取 content
        :param filePath: 文件包含路径
        :return:content
        '''
        with open(filePath, 'rb') as fp:
            return fp.read()

    def read_pcm(self, filename):
        '''
        识别pcm语音文件 转文字
        :param filename: 文件名称
        :return: 识别结果
        '''
        result = self.client.asr(self.get_file_content(filename), 'pcm', 16000, {'dev_pid': 1537, })
        # baidu-api没想到这么脆弱！
        try:
            if result['err_msg'] == 'success.':
                word = result['result'][0] + "\n\n"
            else:
                word = str(result['err_no']) + str(result['err_msg']) + "\n\n"
        except:
            word = str(result) + "\n\n"
        # print(word)
        return word, result['err_no']

    def GoWalkPath(self, path):
        '''
        获取所有文件夹的地址
        '''
        videoPathList = []
        print(path)
        for f_path, dir_name, f_names in os.walk(path):
            if f_path != path:
                videoPathList.append(f_path)
                # print(f_path)
        return videoPathList

    def main(self, path):
        '''
        运行语音转文字并保持word文档
        '''
        pathList = self.GoWalkPath(path)
        print(pathList)
        if len(pathList) > 0:
            for _path in pathList:
                files = self.get_path_files(_path)
                for i in range(0, len(files)):
                    print("baidu")
                    self.baidApi(files[i])
        else:
            print("目录下无文件夹")

    def baidApi(self, path):
        url = "https://vop.baidu.com/server_api"
        # speech 可以通过 get_file_content_as_base64("C:\fakepath\mp4-new.pcm",False) 方法获取
        print(self.fmt)
        payload = json.dumps({
            "format": self.fmt,
            "rate": 16000,
            "channel": 1,
            "cuid": "ORBolw9rb88I4x4uHcLDDi1b6VWmusNP",
            "token": self.access_token,
            "speech": self.get_file_content_as_base64(path, False),
            "len": os.path.getsize(path)
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(json.loads(response.text))
        if response.status_code == 200:
            resp = response.json()
            print(resp)
            if resp["err_no"] == 0:
                result = resp["result"]
                for resut in result:
                    success.write(resut)

        print(response.text)

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": "a2W5jGYEwVz7PVLZVqu458HR",
                  "client_secret": "kz5zcoBxCNWmm3yeuofbs37KQOUm3gfF"}
        return str(requests.post(url, params=params).json().get("access_token"))

    def get_file_content_as_base64(self, path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content


if __name__ == '__main__':
    # pcm 音频路径
    path = "video"
    t = AudioToText()
    print(os.path.abspath(path))
    t.main(os.path.abspath(path))

