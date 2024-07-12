import base64
import urllib
import requests
import json
import os

success = open("success.txt", mode='w', encoding='utf8')
def main(path):
    url = "https://vop.baidu.com/server_api"
    # speech 可以通过 get_file_content_as_base64("C:\fakepath\mp4-new.pcm",False) 方法获取
    payload = json.dumps({
        "format": "pcm",
        "rate": 16000,
        "channel": 1,
        "cuid": "ORBolw9rb88I4x4uHcLDDi1b6VWmusNP",
        "token": get_access_token(),
        "speech": get_file_content_as_base64(path, False),
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
        if resp["err_no"] == 0:
            result = resp["result"]
            for resut in result:
                success.write(resut)

    print(response.text)


def get_file_content_as_base64(path, urlencoded=False):
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

def get_path_files(path, type='.pcm'):
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
            pathFile = os.path.join(path,i)
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

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": "a2W5jGYEwVz7PVLZVqu458HR", "client_secret": "kz5zcoBxCNWmm3yeuofbs37KQOUm3gfF"}
    return str(requests.post(url, params=params).json().get("access_token"))

def GoWalkPath(path):
    '''
    获取所有文件夹的地址
    '''
    videoPathList = []
    for f_path, dir_name, f_names in os.walk(path):
        if  f_path != path:
            videoPathList.append(f_path)
            # print(f_path)
    return videoPathList

def mostOnePcm(path):
    '''
    运行语音转文字并保持word文档
    '''
    pathList = GoWalkPath(path)
    if len(pathList) > 0:
        for _path in pathList:
            files = get_path_files(_path)
            for i in range(0, len(files)):
                main(files[i])
    else:
        print("目录下无文件夹")

if __name__ == '__main__':
    path = "pcm1"
    main(path)
