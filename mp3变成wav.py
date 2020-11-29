# -*-encoding:utf-8-*-
"""
# function/功能 : 
# @File : mp3变成wav.py 
# @Time : 2020/11/29 10:09 
# @Author : kf
# @Software: PyCharm
"""
import numpy as np
from pydub import AudioSegment


def mp32wav(from_path, to_path, frame_rate=16000):
    # from_path: 目标音频文件路径
    # to_path: 转码后文件路径
    # frame_rate: 默认16kHz，可以frame_rate=8000，既8kHz
    mp3_version = AudioSegment.from_mp3(from_path)  # 可以根据文件不太类型导入不同from方法
    # ogg_version = AudioSegment.from_ogg("never_gonna_give_you_up.ogg")
    # flv_version = AudioSegment.from_flv("never_gonna_give_you_up.flv")
    mono = mp3_version.set_frame_rate(frame_rate).set_channels(1)  # 设置声道和采样率
    mono.export(to_path, format='wav', codec='pcm_s16le')  # codec此参数本意是设定16bits pcm编码器, 但发现此参数可以省略


def wav2pcm(wavfile, pcmfile, data_type=np.int16):
    f = open(wavfile, "rb")
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype=data_type)
    data.tofile(pcmfile)


def trans_mp3_to_wav(filepath, filepath2):
    song = AudioSegment.from_mp3(filepath)
    song.export(filepath2, format="wav")

# oldPath='./audio/韩红 - 家乡.mp3'
# newPath="./audio/韩红 - 家乡.wav"
# wavfile="./audio/韩红 - 家乡.wav"
# pcmfile="./audio/韩红 - 家乡.pcm"

wavfile="./audio/16k.wav"
pcmfile="./audio/16k.pcm"
# mp32wav(oldPath,newPath)
wav2pcm(wavfile, pcmfile)
