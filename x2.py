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

os.remove(r'识别结果.txt')
file_name = r'./audio/白杨礼赞.mp3'


def sound_cut(file_name, cut_song_num):
    sound = AudioSegment.from_mp3(file_name)
    # 单位：ms
    stat_time = 0
    end_time = 59

    for i in range(cut_song_num):
        if i == cut_song_num - 1:  # 判断如果是最后一次截断
            cut_song = sound[stat_time * 1000:]  # 截取到最后的时间
        else:
            cut_song = sound[stat_time * 1000:end_time * 1000]
        save_name = r"temp-" + str(i + 1) + '.mp3'  # 设置文件保存名称
        save_name_pcm = r"temp-" + str(i + 1) + '.pcm'  # 设置文件保存名称
        cut_song.export(save_name, format="mp3")  # 进行切割
        order_ffmpeg = 'ffmpeg -i {} -f s16le -ar 16000 -ac 1 -acodec pcm_s16le {}'.format(save_name, save_name_pcm)
        os.system(order_ffmpeg)  # 使用ffmpeg命令转化mp3为pcm
        context = baidu_Speech_To_Text(save_name_pcm)
        with open(r'识别结果.txt', 'a', encoding='utf-8') as f:
            f.write(context)
        os.remove(save_name)  # 删除mp3文件
        os.remove(save_name_pcm)
        # 切割完加入下一段的参数
        stat_time += 59
        end_time += 59
        print(save_name, 'end_time=', stat_time, 'end_time=', end_time)


def get_sond_info(file_name):
    song = mediainfo(file_name)
    song_length = str(int(float(song['duration'])))  # 读取文件时长
    song_size = str(round(float(int(song['size']) / 1024 / 1024), 2)) + 'M'  # 读取文件大小保留两位小数round(变量,2)
    song_filename = song['filename']  # 读取文件地址
    song_format_name = song['format_name']  # 读取文件格式
    try:
        song_name = song['TAG']['title']  # 读取标题
        song_artist = song['TAG']['artist']  # 读取作家
    except:
        song_name = '暂无'
        song_artist = '暂无'

    print('歌名：', song_name, '\n作家', song_artist, '\n歌曲长度', song_length, '\n文件大小', song_size, '\n文件路径', song_filename,
          '\n文件格式', song_format_name)
    cut_song_num = int(int(song_length) / 59) + 1  # 每段59s，计算切割段数
    print('切割次数', cut_song_num)
    return cut_song_num


def baidu_Speech_To_Text(filePath):  # 百度语音识别
    APP_ID = '23061756'
    API_KEY = 'vYSaUlHjkyVwaUujC9G4N1iG'
    SECRET_KEY = 'tA0jokPNLVH133cjNN5jQdCOsAOGaYgj'
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 初始化AipSpeech对象
    # 读取文件
    with open(filePath, 'rb') as fp:
        audioPcm = fp.read()

    json = aipSpeech.asr(audioPcm, 'pcm', 16000, {
        'dev_pid': 1537,
    })
    print(json['err_msg'])
    if 'success' in json['err_msg']:
        context = json['result'][0]
        print('成功，返回结果为：', context)
    else:
        context = '=====识别失败====='
        print('识别失败！')
    return context


cut_song_num = get_sond_info(file_name)
sound_cut(file_name, cut_song_num)
