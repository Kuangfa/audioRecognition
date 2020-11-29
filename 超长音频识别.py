# -*-encoding:utf-8-*-
"""
# function/功能 : 
# @File : x2.py 
# @Time : 2020/11/29 10:18 
# @Author : kf
# @Software: PyCharm
"""
import os

from aip import AipSpeech
from pydub import AudioSegment
from pydub.utils import mediainfo


def sound_cut(file_name):
    if os.path.exists('识别结果.txt'):
        os.remove(r'识别结果.txt')
    song = mediainfo(file_name)
    song_length = str(int(float(song['duration'])))  # 读取文件时长
    song_size = str(round(float(int(song['size']) / 1024 / 1024), 2)) + 'M'  # 读取文件大小保留两位小数round(变量,2)
    song_filename = song['filename']  # 读取文件地址
    song_format_name = song['format_name']  # 读取文件格式
    print('\t长度', song_length, '\t文件大小', song_size, '\t文件路径', song_filename, '\t文件格式', song_format_name)
    cut_song_num = int(int(song_length) / 59) + 1  # 每段59s，计算切割段数
    print('切割次数', cut_song_num)
    sound = AudioSegment.from_mp3(file_name)
    # 单位：ms
    stat_time = 0
    end_time = 59
    for i in range(cut_song_num):
        if i == cut_song_num - 1:  # 判断如果是最后一次截断
            cut_song = sound[stat_time * 1000:]  # 截取到最后的时间
            end_time=int(song_length)
        else:
            cut_song = sound[stat_time * 1000:end_time * 1000]
        save_name = r"temp-" + str(i + 1) + '.mp3'  # 设置文件保存名称
        cut_song.export(save_name, format="mp3")  # 进行切割
        save_name_pcm = r"temp-" + str(i + 1) + '.wav'  # 设置文件保存名称
        mp3_version = AudioSegment.from_mp3(save_name)  # 可以根据文件不太类型导入不同from方法
        mono = mp3_version.set_frame_rate(16000).set_channels(1)  # 设置声道和采样率
        mono.export(save_name_pcm, format='wav', codec='pcm_s16le')  # codec此参数本意是设定16bits pcm编码器, 但发现此参数可以省略
        context = baidu_Speech_To_Text(save_name_pcm)
        with open(r'识别结果.txt', 'a', encoding='utf-8') as f:
            f.write(context)
        os.remove(save_name)  # 删除mp3文件
        os.remove(save_name_pcm)  # 删除mp3文件
        print(save_name, 'end_time=', stat_time, 'end_time=', end_time)
        # 切割完加入下一段的参数
        stat_time += 59
        end_time += 59


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
    print(json['err_msg'])
    if 'success' in json['err_msg']:
        context = json['result'][0]
        print('成功，返回结果为：', context)
    else:
        context = '=====识别失败====='
        print('识别失败！')
    return context


file_name = r'./audio/世间最美的坟墓.mp3'
sound_cut(file_name)
