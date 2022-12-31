from selenium import webdriver
import time
import pyautogui
import os

import re
from pyquery import PyQuery as pq
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   合成小语种需要传输小语种文本、使用小语种发音人vcn、tte=unicode以及修改文本编码方式
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import pyaudio

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

message1 = "现在是空的"

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import yaml
import numpy as np
from matplotlib import pyplot as plt
import pyaudio
import wave


#todo:1完善隐藏
#todo:2处理验证
#讯飞的api

STATUS_FIRST_FRAME1 = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME1 = 1  # 中间帧标识
STATUS_LAST_FRAME1 = 2  # 最后一帧的标识

res = ""
print(1)

yamlPath="config.yaml"

f = open(yamlPath,'r',encoding='utf-8')

cont = f.read()

cont=yaml.safe_load(cont)
print(cont['APPID'])
class Ws_Param1(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1, "vad_eos": 10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket消息的处理
def on_message1(ws, message):
    global res
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

        else:
            data = json.loads(message)["data"]["result"]["ws"]
            # print(json.loads(message))
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]
            print("sid:%s call success!,data is:%s" % (sid, result))
            res += result
    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error1(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close1(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open1(ws):
    def run(*args):
        frameSize = 8000  # 每一帧的音频大小
        intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME1  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open('1230.wav', "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME1
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME1:
                    global cont
                    d = {"common": {"app_id": cont['APPID']},
                         "business": {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1,
                                      "vad_eos": 10000},
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME1
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME1:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME1:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())


def totext():
    # reco()
    # 测试时候在此处正确填写相关信息即可运行
    time1 = datetime.now()
    global cont
    wsParam1 = Ws_Param1(APPID=cont['APPID'], APISecret=cont['APISecret'],
                         APIKey=cont['APIKey'],
                         AudioFile='1230.wav')
    websocket.enableTrace(False)
    wsUrl1 = wsParam1.create_url()
    ws1 = websocket.WebSocketApp(wsUrl1, on_message=on_message1, on_error=on_error1, on_close=on_close1)
    ws1.on_open = on_open1
    ws1.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    time2 = datetime.now()
    print(time2 - time1)
    print(res)
    send(browser, res)


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        # 使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        # self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:

            with open('./demo.pcm', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        global cont
        d = {"common": {"app_id":cont['APPID']},
             "business": {"aue": "raw", "speed": 80, "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"},
             "data": {"status": 2, "text": str(base64.b64encode(message1.encode('utf-8')), "UTF8")},
             }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./demo.pcm'):
            os.remove('./demo.pcm')

    thread.start_new_thread(run, ())


import wave


def pcm2wav(pcm_file, wav_file, channels=1, bits=16, sample_rate=16000):
    # 打开 PCM 文件
    pcmf = open(pcm_file, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()

    # 打开将要写入的 WAVE 文件
    wavfile = wave.open(wav_file, 'wb')
    # 设置声道数
    wavfile.setnchannels(channels)
    # 设置采样位宽
    wavfile.setsampwidth(bits // 8)
    # 设置采样率
    wavfile.setframerate(sample_rate)
    # 写入 data 部分
    wavfile.writeframes(pcmdata)
    wavfile.close()


def player(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)
    # print(data)
    while data != b'':
        data = wf.readframes(chunk)
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()


def play(message):
    # 测试时候在此处正确填写相关信息即可运行
    global cont
    wsParam = Ws_Param(APPID=cont['APPID'], APISecret=cont['APPID'],
                       APIKey=cont['APIKey'],
                       Text=message)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    pcm2wav("demo.pcm", "demo.wav")
    audiofile = "demo.wav"
    player(audiofile)


def killcookie(driver,message):
    cookies = driver.get_cookies()
    for each in cookies:
        if("openai" in each['domain']):
            driver.delete_cookie(each["name"])
    driver.refresh()
    yn = 1
    while yn == 1:
        time.sleep(5)
        try:
            WebDriverWait(driver, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                            'button[class="btn flex justify-center gap-2 btn-primary"]'))
            yn = 2
        except:
            pass
        try:
            WebDriverWait(browser, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                          'input[value="Verify you are human"]'))
            browser.find_element(By.CSS_SELECTOR, 'input[value="Verify you are human"]').click()
            time.sleep(1)
            browser.execute_script('window.open("https://chat.openai.com/chat")')
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
        except:
            pass
        try:
            WebDriverWait(browser, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                          'div[class="hcaptcha-box"]'))
            browser.find_element(By.CSS_SELECTOR, 'div[class="hcaptcha-box"]').click()
            time.sleep(1)
            browser.execute_script('window.open("https://chat.openai.com/chat")')
            windows = browser.window_handles
            browser.switch_to.window(windows[-1])
        except:
            pass

    print(1)
    windows = driver.window_handles  # 获取所有句柄
    driver.switch_to.window(windows[1])  # 切换到句柄为1的标签页
    WebDriverWait(driver, 1000, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                    'button[class="btn flex justify-center gap-2 btn-primary"]'))
    time.sleep(5)
    driver.close()
    driver.switch_to.window(windows[0])

    driver.refresh()
    WebDriverWait(driver, 1000, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                 'button[class="btn flex justify-center gap-2 btn-primary"]'))
    driver.find_element(By.CSS_SELECTOR,'button[class="btn flex justify-center gap-2 btn-primary"]').click()
    WebDriverWait(driver, 1000, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                    '[type="submit"][data-provider="google"]'))
    driver.find_element(By.CSS_SELECTOR, '[type="submit"][data-provider="google"]').click()

    WebDriverWait(driver, 1000, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                    'div[data-identifier="lhy770422@gmail.com"]'))
    driver.find_element(By.CSS_SELECTOR, 'div[data-identifier="lhy770422@gmail.com"]').click()
    try:
        WebDriverWait(driver, 4, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                        'button[class="btn flex justify-center gap-2 btn-neutral ml-auto"]'))
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn flex justify-center gap-2 btn-neutral ml-auto"]').click()
        WebDriverWait(driver, 4, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                        'button[class="btn flex justify-center gap-2 btn-neutral ml-auto"]'))
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn flex justify-center gap-2 btn-neutral ml-auto"]').click()
        WebDriverWait(driver, 4, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                        'button[class="btn flex justify-center gap-2 btn-primary ml-auto"]'))
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn flex justify-center gap-2 btn-primary ml-auto"]').click()
    except:
        pass
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'textarea[tabindex="0"]').send_keys(message)
    driver.find_element(By.CSS_SELECTOR,
                        'button[class="absolute p-1 rounded-md text-gray-500 bottom-1.5 right-1 md:bottom-2.5 md:right-2 hover:bg-gray-100 dark:hover:text-gray-400 dark:hover:bg-gray-900 disabled:hover:bg-transparent dark:disabled:hover:bg-transparent"]').click()
    a = 1
    while a == 1:
        html = driver.page_source
        data = str(pq(html))
        ans3 = re.findall(
            'class="flex flex-grow flex-([\s\S]*?)div>', data)
        if ans3 != None:
            ans3 = ans3[-1]
            ans5 = re.findall('<p>([\s\S]*?)</p>', ans3)
            ans4 = ""
            for each in ans5:
                ans4 += each
            global text
        try:
            print("in2")

            WebDriverWait(driver, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                         'button[class="btn flex justify-center gap-2 btn-neutral border-0 md:border"]'))
            a = 2
        except:
            pass
        print("in3")
        html = driver.page_source
        data = str(pq(html))
        if "There was an error generating a response" in data:
            killcookie(driver, message)
            a = 2

        print("in")
def send(driver, message):
    driver.find_element(By.CSS_SELECTOR, 'textarea[tabindex="0"]').send_keys(message)
    driver.find_element(By.CSS_SELECTOR,
                        'button[class="absolute p-1 rounded-md text-gray-500 bottom-1.5 right-1 md:bottom-2.5 md:right-2 hover:bg-gray-100 dark:hover:text-gray-400 dark:hover:bg-gray-900 disabled:hover:bg-transparent dark:disabled:hover:bg-transparent"]').click()
    a=1
    while a==1:
        html = driver.page_source
        data = str(pq(html))
        ans3 = re.findall(
            'class="flex flex-grow flex-([\s\S]*?)div>', data)
        if ans3!=None:
            ans3=ans3[-1]
            ans5 = re.findall('<p>([\s\S]*?)</p>', ans3)
            ans4 = ""
            for each in ans5:
                ans4 += each
            global text
            text.set(len(ans4))
        try:
            print("in2")

            WebDriverWait(driver, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                    'button[class="btn flex justify-center gap-2 btn-neutral border-0 md:border"]'))
            a=2
        except:
            pass
        print("in3")
        html = driver.page_source
        data = str(pq(html))
        if "There was an error generating a response" in data:
            killcookie(driver, message)
            a=2

        print("in")

    html = driver.page_source
    data = str(pq(html))
    ans1 = re.findall(
        'class="flex flex-grow flex-([\s\S]*?)div>',data)[-1]
    print(ans1)
    ans = re.findall('<p>([\s\S]*?)</p>', ans1)
    ans2 = ""
    for each in ans:
        ans2 += each
    print(ans2)
    global message1
    message1 = ans2
    print(message1)
    play(ans2)


import numpy as np
from matplotlib import pyplot as plt
import pyaudio
import wave
import tkinter
import threading


def endd():
    global flag
    flag = False


def start():  # 键位1start
    global flag
    flag = True
    threads = []  # 双线程 录音和结束判断
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


def reco():
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    fs = 16000
    duration = 14400
    channels = 1
    n = duration * fs
    t = np.arange(1, n) / fs
    wave_output_file = '1230.wav'
    # print('这段音频有几秒：', duration)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=channels, rate=fs,
                    input=True, frames_per_buffer=CHUNK)
    print('开始录制：')

    frames = []
    for i in range(0, int(fs / CHUNK * duration)):
        if flag != False:
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
    global res
    res = ""
    totext()


flag = True
root = tkinter.Tk()

root['height'] = 140
root['width'] = 300
buttonOk = tkinter.Button(root,
                          text='START',
                          activeforeground='#ff0000',
                          command=start)
buttonOk.place(x=30, y=30, width=100, height=30)
root.title('小助手')
text = tkinter.StringVar()
text.set("无")
label = tkinter.Label(root,textvariable=text,anchor="se")
label.place(x=200,y=100)
#label.pack()



task = 'chrome --remote-debugging-port=8100 --user-data-dir="G:\chrome_config"'
import os

p = os.popen(task, 'r')

"""
pyautogui.keyDown('winleft')
pyautogui.press('r')
pyautogui.keyUp('winleft')
pyautogui.press('enter')

time.sleep(0.3)

pyautogui.keyDown('ctrlleft')
pyautogui.keyDown('shiftleft')
pyautogui.keyUp('ctrlleft')
pyautogui.keyUp('shiftleft')


for each in task:
    pyautogui.press(each)

time.sleep(0.3)
pyautogui.press('enter')
"""
""""""
print(1)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8100")
print(1)
browser = webdriver.Chrome(chrome_options=chrome_options)
print(1)
browser.set_page_load_timeout(100)
#browser.get("http://javabin.cn/bot/bot.html")
browser.get("https://chat.openai.com/chat")
"""
time.sleep(1)
yn=1
while yn==1:
    time.sleep(5)
    try:
        WebDriverWait(browser, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                        'div[class="flex flex-col w-full py-2 pl-3 flex-grow md:py-3 md:pl-4 relative border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark:bg-gray-700 rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)] dark:shadow-[0_0_15px_rgba(0,0,0,0.10)]"]'))

        yn=2
    except:
        pass
    try:
        WebDriverWait(browser, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                     'input[value="Verify you are human"]'))
        browser.find_element(By.CSS_SELECTOR,'input[value="Verify you are human"]').click()
        time.sleep(1)
        browser.execute_script('window.open("https://chat.openai.com/chat")')
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
    except:
        pass
    try:
        WebDriverWait(browser, 2, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                     'div[class="hcaptcha-box"]'))
        browser.find_element(By.CSS_SELECTOR, 'div[class="hcaptcha-box"]').click()
        time.sleep(1)
        browser.execute_script('window.open("https://chat.openai.com/chat")')
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
    except:
        pass

print(1)
windows = browser.window_handles  # 获取所有句柄
while(len(windows)>1):
    browser.switch_to.window(windows[-1])
    browser.close()
    windows = browser.window_handles  # 获取所有句柄

browser.switch_to.window(windows[0])
"""
browser.refresh()
WebDriverWait(browser, 10000, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR,
                                                                'div[class="flex flex-col w-full py-2 pl-3 flex-grow md:py-3 md:pl-4 relative border border-black/10 bg-white dark:border-gray-900/50 dark:text-white dark:bg-gray-700 rounded-md shadow-[0_0_10px_rgba(0,0,0,0.10)] dark:shadow-[0_0_15px_rgba(0,0,0,0.10)]"]'))

send(browser, "之后的对话你只能用一个最多100字，同时不要使用<li>标签，并用中文回答，如果懂了那就回复：初始化")


root.mainloop()
"""
"""