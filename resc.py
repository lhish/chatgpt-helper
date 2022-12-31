import numpy as np
from matplotlib import pyplot as plt
import pyaudio
import wave
import tkinter
import threading

def endd():
    global flag
    flag=False
    
def start():#键位1start
    global flag
    flag=True
    threads=[]#双线程 录音和结束判断
    t1 = threading.Thread(target=reco)
    threads.append(t1)
    def end():
        buttonOkk = tkinter.Button(root,
                              text='END',
                              activeforeground='#ff0000',
                              command=endd)
        buttonOkk.place(x=150, y=30, width=100, height=30)
        root.update()
    t2 = threading.Thread(target=end)
    threads.append(t2)
    for t in threads:
        t.start()

def show():#主函数
    global flag
    global root
    flag=True
    root = tkinter.Tk()
    root['height'] = 140
    root['width'] = 300
    buttonOk = tkinter.Button(root,
                          text='START',
                          activeforeground='#ff0000',
                          command=start)
    buttonOk.place(x=30, y=30, width=100, height=30)
    root.mainloop()
    
    
def reco():
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    fs = 16000
    duration = 14400
    channels = 1
    n = duration * fs
    t = np.arange(1, n) / fs
    wave_output_file = '1230.wav'
    #print('这段音频有几秒：', duration)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=channels, rate=fs,
                    input=True, frames_per_buffer=CHUNK)
    print('开始录制：')

    frames = []
    for i in range(0, int(fs / CHUNK * duration)):
        if flag!=False:
            data = stream.read(CHUNK)
            frames.append(data)
        else:
            break

    print('录制结束')
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(wave_output_file, 'wb')  # 打开这个文件，以二进制写入的方式
    wf.setnchannels(channels)  # 设置单声道
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置采样位宽
    wf.setframerate(fs)  # 设置采样率
    wf.writeframes(b''.join(frames))  # 把所有的帧连成一段语音
    wf.close()

