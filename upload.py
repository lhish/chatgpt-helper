# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:17:02 2021

@author: lhy
"""
import os.path
import re
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime





#

def areaj(context,j):
    if j>=10:
        context.send_keys('')
    else:
        context.send_keys('  ')

def addspace(string1):
    a=string1[0]
    inner_code=ord(a)
    if (inner_code >= 0x0020 and inner_code <= 0x7e) or (a >= u'\u4e00' and a <= u'\u9fa5') or a=="‘" or a=="’" or a=='“' or a=='”':
        return '  '+string1
    else:
        return string1



def mainpart():
    filename=datetime.datetime.now().strftime('%Y-%m-%d')+".txt"
    with open(filename, "r",encoding='utf-8') as f:
        lines=f.readlines()
        a=0
        bvinfo=[None]*len(lines)
        for line in lines:
            oldinfo1={}
            oldinfo1['url']=re.findall("{'url': '(.*?)', '",line)[0]
            oldinfo1['area1']=re.findall("', 'area1': '(.*?)', '",line)[0]
            oldinfo1['area2']=re.findall("', 'area2': '(.*?)', '",line)[0]
            oldinfo1['author']=re.findall("', 'author': '(.*?)', '",line)[0]
            oldinfo1['title']=re.findall("', 'title': (.*?)}",line)[0]
            oldinfo1['title']=oldinfo1['title'][1:-1]
            bvinfo[a]=oldinfo1
            a=a+1
    

    url='https://member.bilibili.com/platform/upload/text/edit'
    url1='https://member.bilibili.com/platform/upload/text/draft'
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8210")
    browser  = webdriver.Chrome(chrome_options=chrome_options)
    try:
        browser.maximize_window()
    except:
        a=1
        
    browser.get(url1)
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('h2[class="head-title title"]'))
    a=len(browser.find_elements_by_css_selector('button[class="bili-btn plain"]'))
    while(a>0):
        browser.find_element_by_css_selector('button[class="bili-btn plain"]').click()
        time.sleep(0.2)
        browser.find_elements_by_css_selector('button[class="bili-btn ok"]')[-1].click()
        time.sleep(0.2)
        a=len(browser.find_elements_by_css_selector('button[class="bili-btn plain"]'))
    
    browser.get(url)
    
    time.sleep(2)
    
    
    
    browser.switch_to.default_content() 
    frame = browser.find_elements_by_tag_name('iframe')[1]  
    browser.switch_to.frame(frame) 
    
    html=browser.page_source
    data=str(pq(html))
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('textarea[placeholder="请输入标题（建议30字以内）"]'))
    title=datetime.datetime.now().strftime('%m月%d日')+"热门"
    browser.find_element_by_css_selector('textarea[placeholder="请输入标题（建议30字以内）"]').send_keys(Keys.CONTROL,'a')
    time.sleep(0.3)
    browser.find_element_by_css_selector('textarea[placeholder="请输入标题（建议30字以内）"]').send_keys(Keys.DELETE)
    browser.find_element_by_css_selector('textarea[placeholder="请输入标题（建议30字以内）"]').send_keys(title)
    
    
    icon=browser.find_element_by_css_selector('li[class="toolbar-item left hover-show-childs has-childs"]')
    mostbig=browser.find_element_by_css_selector('li.t4>i.icon-text')
    morebig=browser.find_element_by_css_selector('li.t3>i.icon-text')
    normalbig=browser.find_element_by_css_selector('li.t2>i.icon-text')
    smallbig=browser.find_element_by_css_selector('li.t1>i.icon-text')
    stoke=browser.find_element_by_css_selector('i[class="icon-font parent-icon icon-bold"]')
    superlink=browser.find_element_by_css_selector('i[class="icon-font parent-icon icon-link"]')
    frame = browser.find_elements_by_tag_name('iframe')[0]  
    browser.switch_to.frame(frame) 
    
    try:
        WebDriverWait(browser,10,0.2).until(lambda x:x.find_element_by_css_selector('p[class="origin-placeholder"]'))
    except:
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.CONTROL,'a')
        time.sleep(0.3)
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.DELETE)
        time.sleep(0.3)
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.CONTROL,'a')
        time.sleep(0.3)
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.DELETE)
        time.sleep(0.3)
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.CONTROL,'a')
        time.sleep(0.3)
        browser.find_element_by_css_selector('body[contenteditable="true"]').send_keys(Keys.DELETE)
    
    contextarea=browser.find_element_by_css_selector('body[contenteditable="true"]')
    eachbefore={}
    i=0
    j=1
    
    html=browser.page_source
    data=str(pq(html))
    
    for each in bvinfo:
        time.sleep(0.2)
        if i!=0:
            if each['area1']!=eachbefore['area1']:
                j=1
                contextarea.send_keys('\n')
                time.sleep(0.2)
                browser.switch_to.parent_frame()
            
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                mostbig.click()
                
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(each['area1'])
                contextarea.send_keys(Keys.HOME)
                time.sleep(0.1)            
                contextarea.send_keys(Keys.SHIFT,Keys.END)
                time.sleep(0.1)
                browser.switch_to.parent_frame()
                stoke.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(Keys.END)
                browser.switch_to.parent_frame()
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys('\n')
                time.sleep(0.2)
                
                browser.switch_to.parent_frame()
                
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                normalbig.click()
                
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(each['area2'])
                browser.switch_to.parent_frame()
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                stoke.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys('\n')
                time.sleep(0.2)
                areaj(contextarea,j)
                contextarea.send_keys(str(j)+'.')
                contextarea.send_keys(Keys.HOME)
                time.sleep(0.1)
                contextarea.send_keys(Keys.SHIFT,Keys.END)
                time.sleep(0.1)
                browser.switch_to.parent_frame()
                superlink.click()
                time.sleep(0.2)
                browser.find_element_by_css_selector('input[placeholder="请输入站内链接"]').send_keys(each['url'])
                WebDriverWait(browser,10,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
                browser.find_element_by_css_selector('button[class="ui-btn blue-radius"]').click()
                time.sleep(0.1)
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(addspace(re.sub(u"([^\u0000-\uffff])","",each['title']))+' ----'+re.sub(u"([^\u0000-\uffff])","",each['author'])+'\n')
                time.sleep(0.2)
            elif each['area2']!=eachbefore['area2']:
                j=1
                browser.switch_to.parent_frame()
            
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                normalbig.click()
                
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(each['area2'])
                contextarea.send_keys(Keys.HOME)
                time.sleep(0.1)            
                contextarea.send_keys(Keys.SHIFT,Keys.END)
                time.sleep(0.1)
                browser.switch_to.parent_frame()
                stoke.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(Keys.END)
                browser.switch_to.parent_frame()
                stoke.click()
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys('\n')
                time.sleep(0.2)
                areaj(contextarea,j)
                contextarea.send_keys(str(j)+'.')
                contextarea.send_keys(Keys.HOME)
                time.sleep(0.1)
                contextarea.send_keys(Keys.SHIFT,Keys.END)
                time.sleep(0.1)
                browser.switch_to.parent_frame()
                superlink.click()
                time.sleep(0.2)
                browser.find_element_by_css_selector('input[placeholder="请输入站内链接"]').send_keys(each['url'])
                WebDriverWait(browser,10,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
                browser.find_element_by_css_selector('button[class="ui-btn blue-radius"]').click()
                time.sleep(0.1)
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(addspace(re.sub(u"([^\u0000-\uffff])","",each['title']))+' ----'+re.sub(u"([^\u0000-\uffff])","",each['author'])+'\n')
                time.sleep(0.2)
            else:
                areaj(contextarea,j)
                contextarea.send_keys(str(j)+'.')
                contextarea.send_keys(Keys.HOME)
                time.sleep(0.1)
                contextarea.send_keys(Keys.SHIFT,Keys.END)
                time.sleep(0.1)
                browser.switch_to.parent_frame()
                superlink.click()
                time.sleep(0.2)
                browser.find_element_by_css_selector('input[placeholder="请输入站内链接"]').send_keys(each['url'])
                WebDriverWait(browser,10,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
                browser.find_element_by_css_selector('button[class="ui-btn blue-radius"]').click()
                time.sleep(0.1)
                ActionChains(browser).move_to_element(icon).perform()
                time.sleep(0.1)
                smallbig.click()
                frame = browser.find_elements_by_tag_name('iframe')[0]  
                browser.switch_to.frame(frame)
                contextarea.send_keys(addspace(re.sub(u"([^\u0000-\uffff])","",each['title']))+' ----'+re.sub(u"([^\u0000-\uffff])","",each['author'])+'\n')
                time.sleep(0.2)
        else:
            
            browser.switch_to.parent_frame()
            
            ActionChains(browser).move_to_element(icon).perform()
            mostbig.click()
            
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys(each['area1'])
            contextarea.send_keys(Keys.HOME)
            time.sleep(0.1)            
            contextarea.send_keys(Keys.SHIFT,Keys.END)
            time.sleep(0.1)
            browser.switch_to.parent_frame()
            stoke.click()
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys(Keys.END)
            browser.switch_to.parent_frame()
            ActionChains(browser).move_to_element(icon).perform()
            smallbig.click()
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys('\n')
            time.sleep(0.2)
            
            
            browser.switch_to.parent_frame()
            
            ActionChains(browser).move_to_element(icon).perform()
            time.sleep(0.1)
            normalbig.click()
            
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys(each['area2'])
            browser.switch_to.parent_frame()
            ActionChains(browser).move_to_element(icon).perform()
            time.sleep(0.1)
            smallbig.click()
            stoke.click()
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys('\n')
            time.sleep(0.2)
            areaj(contextarea,j)
            contextarea.send_keys(str(j)+'.')
            contextarea.send_keys(Keys.HOME)
            time.sleep(0.1)
            contextarea.send_keys(Keys.SHIFT,Keys.END)
            time.sleep(0.1)
            browser.switch_to.parent_frame()
            superlink.click()
            time.sleep(0.2)
            browser.find_element_by_css_selector('input[placeholder="请输入站内链接"]').send_keys(each['url'])
            WebDriverWait(browser,10,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
            browser.find_element_by_css_selector('button[class="ui-btn blue-radius"]').click()
            time.sleep(0.1)
            ActionChains(browser).move_to_element(icon).perform()
            time.sleep(0.1)
            smallbig.click()
            frame = browser.find_elements_by_tag_name('iframe')[0]  
            browser.switch_to.frame(frame)
            contextarea.send_keys(addspace(re.sub(u"([^\u0000-\uffff])","",each['title']))+' ----'+re.sub(u"([^\u0000-\uffff])","",each['author'])+'\n')
            time.sleep(0.2)
        eachbefore=each
        i=i+1
        j=j+1
        
    
    browser.switch_to.parent_frame()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('a[class="repick default-repick"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('a[class="repick default-repick"]').click()
    time.sleep(1)
    os.system("choose-file.exe")
    
    time.sleep(0.5)
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('button[class="ui-btn blue-radius"]')[1].click()
    
    time.sleep(0.5)
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('input[type="checkbox"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('input[type="checkbox"]')[-1].click()
    
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius original-btn"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('button[class="ui-btn blue-radius original-btn"]').click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('div[class="show-more-btn"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('div[class="show-more-btn"]').click()
    
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn sub-btn create-btn"'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('button[class="ui-btn sub-btn create-btn"').click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('input[type="radio"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('input[type="radio"]')[4].click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius main-btn"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('button[class="ui-btn blue-radius main-btn"]').click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('input[class="ui-input add-control"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('input[class="ui-input add-control"]').send_keys("热门")
    browser.find_element_by_css_selector('input[class="ui-input add-control"]').send_keys(Keys.ENTER)
    browser.find_element_by_css_selector('input[class="ui-input add-control"]').send_keys("数据分类")
    browser.find_element_by_css_selector('input[class="ui-input add-control"]').send_keys(Keys.ENTER)
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('div[class="check-radio-v2-2-container"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('div[class="check-radio-v2-2-container"]').click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('div[class="date-picker-timer"]'))
    time.sleep(0.2)
    browser.find_element_by_css_selector('div[class="date-picker-timer"]').click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('span[class="time-picker-panel-select-item"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('span[class="time-picker-panel-select-item"]')[20].click()
    
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('span[class="time-picker-panel-select-item"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('span[class="time-picker-panel-select-item"]')[-6].click()
    """
    WebDriverWait(browser,100,0.2).until(lambda x:x.find_element_by_css_selector('button[class="ui-btn blue-radius"]'))
    time.sleep(0.2)
    browser.find_elements_by_css_selector('button[class="ui-btn blue-radius"]')[-1].click()
    """

a=-1
while a==-1:
    a=1
    try:
        mainpart()
    except:
        a=-1