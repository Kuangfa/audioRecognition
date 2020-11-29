#-*-encoding:utf-8-*-
"""
# function/功能 : 
# @File : 百度语音识别示例.py 
# @Time : 2020/11/29 9:36 
# @Author : kf
# @Software: PyCharm
"""

from aip import AipSpeech



def baidu_Speech_To_Text(filePath):  # 百度语音识别
    """ 你的 APPID AK SK """
    APP_ID = '你的 App ID'
    API_KEY = '你的 Api Key'
    SECRET_KEY = '你的 Secret Key'
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 初始化AipSpeech对象
    # 读取文件
    with open(filePath, 'rb') as fp:
        audioPcm = fp.read()
    json = aipSpeech.asr(audioPcm, 'pcm', 16000, {'lan': 'zh', })
    print(json)
    if 'success' in json['err_msg']:
        context = json['result'][0]
        print('成功，返回结果为：', context)
    else:
        context = '=====识别失败====='
        print('识别失败！')
    return context



# oldPath='./audio/韩红 - 家乡.mp3'
oldPath='./audio/16k.pcm'
# oldPath='temp-1.wav'


baidu_Speech_To_Text(oldPath)
