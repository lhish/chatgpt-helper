from selenium import webdriver
import time
import win32gui
import win32con
import re
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import re
import datetime
import os.path
import os
from os import system
import keyboard
import pyautogui
monthday=[0,31,28,31,30,31,30,31,31,30,31,30,31]
def upload():
    filename=datetime.datetime.now().strftime('%Y-%m-%d')+".txt"
    year=int(datetime.datetime.now().strftime('%Y'))
    day=int(datetime.datetime.now().strftime('%d'))
    month=int(datetime.datetime.now().strftime('%m'))
    day=day-1
    if day<1:
        month=month-1
        if month<1:
            month=12
            year=year-1
        day=monthday[month]
    if month<=9 and month>=1:
        monthstr='0'+str(month)
    else:
        monthstr=str(month)
    if day<=9 and day>=1:
        daystr='0'+str(day)
    else:
        daystr=str(day)
    filenamebefore=str(year)+'-'+monthstr+'-'+daystr+'.txt'
    with open(filenamebefore, "r",encoding='utf-8') as f:
        lines=f.readlines()
        a=0
        bvinfo1=[None]*len(lines)
        for line in lines:
            oldinfo1={}
            oldinfo1['url']=re.findall("{'url': '(.*?)', '",line)[0]
            oldinfo1['area1']=re.findall("', 'area1': '(.*?)', '",line)[0]
            oldinfo1['area2']=re.findall("', 'area2': '(.*?)', '",line)[0]
            oldinfo1['author']=re.findall("', 'author': '(.*?)', '",line)[0]
            oldinfo1['title']=re.findall("', 'title': (.*?)}",line)[0]
            oldinfo1['title']=oldinfo1['title'][1:-1]
            bvinfo1[a]=oldinfo1
            a=a+1
    with open(filename, "r",encoding='utf-8') as f:
        lines=f.readlines()
        a=0
        bvinfo2=[None]*len(lines)
        for line in lines:
            oldinfo1={}
            oldinfo1['url']=re.findall("{'url': '(.*?)', '",line)[0]
            oldinfo1['area1']=re.findall("', 'area1': '(.*?)', '",line)[0]
            oldinfo1['area2']=re.findall("', 'area2': '(.*?)', '",line)[0]
            oldinfo1['author']=re.findall("', 'author': '(.*?)', '",line)[0]
            oldinfo1['title']=re.findall("', 'title': (.*?)}",line)[0]
            oldinfo1['title']=oldinfo1['title'][1:-1]
            t=0
            for each in bvinfo1:
                if each['url']==oldinfo1['url']:
                    t=1
            if t==0:
                bvinfo2[a]=oldinfo1
                a=a+1
    
    bvinfo=[None]*a
    b=0
    for each in bvinfo2:
        if each!=None:
            bvinfo[b]=each
            b=b+1
    
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8210")
    browser  = webdriver.Chrome(chrome_options=chrome_options)
    browser.maximize_window()
    a=-1
    while a==-1:
        a=1
        try:
            uploadstatus(bvinfo,browser)
        except:
            a=-1
    
    
def uploadstatus(bvinfohere,browser):
    url2="https://t.bilibili.com/"
    browser.get(url2)
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('div[id="editor"]'))
    time.sleep(0.2)
    contextarea=browser.find_element_by_css_selector('div[id="editor"]')
    contextarea.send_keys('本文是帮助更好更迅速地获知每日热门(每2小时查看一次热门)的信息，仅包括今日热门有且昨日热门没有的视频\n如果有帮助到你，请点个赞，让up主有持续做下去的动力，另外可以在评论区留下改进的建议以及你的看法\n')
    contextarea.send_keys('每日16:00左右更新\n专栏应该6:30分出，但审核的时间过于不确定，故增加了此动态\n')
    eachbefore={'area1':'','area2':''}
    for each in bvinfohere:
        if each['area1']!=eachbefore['area1']:
            contextarea.send_keys(each['area1'])
            contextarea.send_keys('\n')
        if each['area2']!=eachbefore['area2']:
            contextarea.send_keys(each['area2'])
            contextarea.send_keys('\n')
        contextarea.send_keys(each['url'])
        contextarea.send_keys('\n')
        eachbefore=each


upload()