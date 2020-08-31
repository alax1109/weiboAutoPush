from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import re
import win32api
import win32con
import win32gui
import random

"""
深圳地区和仁爱医院病种
"""
sz_loc = './blog/weibo/地区/sz_location.txt'
ra_disease = './blog/weibo/病种/ra_disease_renliu.txt'

"""
厦门地区和鹭港医院病种
"""

xm_loc = './blog/weibo/地区/xm_location.txt'
lg_disease = './blog/weibo/病种/lg_disease_renliu.txt'

"""
东莞地区和东方医院病种
"""
dg_loc = './blog/weibo/地区/dg_location.txt'
df_disease = './blog/weibo/病种/df_disease.txt'
"""
台州
"""
tz_loc = './blog/weibo/地区/tz_location.txt'
tz_disease = './blog/weibo/病种/tz_disease.txt'
"""
宁波
"""
nb_loc = './blog/weibo/地区/nb_location.txt'
nb_disease = './blog/weibo/病种/nb_disease.txt'
"""
温州
"""
wz_loc = './blog/weibo/地区/wz_location.txt'
wz_disease = './blog/weibo/病种/wz_disease.txt'
"""
账号密码
"""
sz_account = ''
"""
修饰词
"""
compose_key = './blog/weibo/组合词/compose_key.txt'
with open('./blog/weibo/随机文章内容/rand_content.txt', 'r', encoding='UTF-8') as rand_s:
    R_string = rand_s.readlines()
    rand_str = random.choice(R_string)
# rand_string = open('/rand_string.txt', 'r', encoding='UTF-8')
# R_string = rand_string.readlines()
# rand_str = random.choice(R_string)


def randString(path):  # 返回文本中随机字符串
    with open(path, 'r') as location:
        loc_content = location.readlines()
        loc_content = [x.strip() for x in loc_content if x.strip() != ""]
    res = random.choice(loc_content)
    return res


ra_push_loc = randString(sz_loc)  # 深圳地域
ra_push_content = randString(ra_disease)  # 仁爱病种

lg_push_loc = randString(xm_loc)  # 厦门地域
lg_push_content = randString(lg_disease)  # 鹭港病种

dg_push_loc = randString(dg_loc)  # 东莞地域
df_push_content = randString(df_disease)  # 东莞病种

tz_push_loc = randString(tz_loc)  # 台州地域
tz_push_content = randString(tz_disease)  # 台州病种

nb_push_loc = randString(nb_loc)  # 宁波地域
nb_push_content = randString(nb_disease)  # 宁波病种

wz_push_loc = randString(wz_loc)  # 温州地域
wz_push_content = randString(wz_disease)  # 温州病种

compose_kw = randString(compose_key)  # 所有关键词修饰定语
ra_total_key = '['+randString(sz_loc) + \
    randString(ra_disease)+randString(compose_key)+']'

ra_img_dir = './blog/weibo/renai_pic/'
ra_img_upload = os.listdir(ra_img_dir)
ra_img_upload.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
img = ra_img_upload[:9]

lg_img_dir = './blog/weibo/lugang_pic'
lg_img_upload = os.listdir(lg_img_dir)
lg_img_upload.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
img = lg_img_upload[:9]

main_dir = os.getcwd()

ra_upload_img_dir = '\\blog\\weibo\\renai_pic'
lg_upload_img_dir = '\\blog\\weibo\\lugang_pic'

with open('./账号/ra_account.txt', 'r', encoding='utf-8-sig') as ra_account:  # 深圳账号
    shenzhen_account = ra_account.readlines()
sz_account = shenzhen_account

with open('./账号/lg_account.txt', 'r', encoding='utf-8-sig') as lg_account:  # 厦门账号
    lugang_account = ra_account.readlines()
xm_account = lugang_account

ra_post_time = 0
lg_post_time = 0

browser = webdriver.Firefox()
browser.get('https://www.weibo.com/')
WebDriverWait(browser, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".info_list.login_btn a[node-type='submitBtn']")))


def login(username, password):
    try:
        browser.find_element_by_css_selector("#loginname").send_keys(username)
        browser.find_element_by_css_selector(
            ".info_list.password input[node-type='password']").send_keys(password)
        browser.find_element_by_css_selector(
            ".info_list.login_btn a[node-type='submitBtn']").click()
    except:
        browser.find_element_by_css_selector("#loginname").clear()
        browser.find_element_by_css_selector(
            ".info_list.password input[node-type='password']").clear()
        sleep(0.5)
        browser.find_element_by_css_selector("#loginname").send_keys(username)
        browser.find_element_by_css_selector(
            ".info_list.password input[node-type='password']").send_keys(password)
        browser.find_element_by_css_selector(
            ".info_list.login_btn a[node-type='submitBtn']").click()


def logout():
    browser.get("https://weibo.com/logout.php?backurl=%2F")
    sleep(3)
    browser.find_element_by_css_selector("#loginname").clear()
    sleep(0.5)
    browser.find_element_by_css_selector(
        ".info_list.password input[node-type='password']").clear()


if len(sz_account) % 4 == 0:
    while len(sz_account) >= 4:
        login(sz_account[-4], sz_account[-3])
        sleep(8)
        while WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                           ".func a[node-type='submit']"))) ra_post_time <= sz_account[-1]:  # 文章发布次数
            sleep(2)
            upload = browser.find_element_by_css_selector(
                'form[id="pic_upload"]').click()
            for up_img in img:
                imgFile = main_dir + ra_upload_img_dir + '\\' + up_img  # 文件图片绝对路径
                dialog = win32gui.FindWindow('#32770', "文件上传")  # 一级
                ComboBoxEx32 = win32gui.FindWindowEx(
                    dialog, 0, 'ComboBoxEx32', None)  # 二级
                ComboBox = win32gui.FindWindowEx(
                    ComboBoxEx32, 0, 'ComboBox', None)  # 三级
                edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 四级
                button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 五级
                win32gui.SendMessage(edit, win32con.WM_SETTEXT,
                                     None, imgFile)  # 循环到最后一次退出上传框
                win32gui.SendMessage(dialog, win32con.WM_COMMAND,
                                     1, button)  # 循环到最后一次退出上传框
                if up_img not in img[len(img)-1]:
                    WebDriverWait(browser, 15).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul>li[class="add"]')))
                    browser.find_element_by_css_selector(
                        'ul>li[class="add"]').click()
            sleep(3)
            ra_total_key1 = '['+randString(sz_loc) + \
                randString(ra_disease)+randString(compose_key)+']'
            ra_total_key2 = '['+randString(sz_loc) + \
                randString(ra_disease)+randString(compose_key)+']'
            ra_total_key3 = '['+randString(sz_loc) + \
                randString(ra_disease)+randString(compose_key)+']'

            ra_content = ra_total_key1+ra_total_key2+'欢迎拨打下方咨询热线' + \
                ra_total_key+rand_str+ra_total_key3  # 动态调用

            browser.find_element_by_css_selector(
                ".input textarea[node-type='textEl']").send_keys(ra_content)
            browser.find_element_by_css_selector(
                ".func a[node-type='submit']").click()
            sleep(3)
            ra_post_time += 1
        logout()
    sz_account.pop()
    sz_account.pop()
    sz_account.pop()
    sz_account.pop()

elif len(xm_account) % 4 == 0:
    while len(xm_account) >= 4:
        login(xm_account[-4], xm_account[-3])
        sleep(8)
        while WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                           ".func a[node-type='submit']"))) lg_post_time <= xm_account[-1]:  # 文章发布次数
            sleep(2)
            upload = browser.find_element_by_css_selector(
                'form[id="pic_upload"]').click()
            for up_img in img:
                imgFile = main_dir + lg_upload_img_dir + '\\' + up_img  # 文件图片绝对路径
                dialog = win32gui.FindWindow('#32770', "文件上传")  # 一级
                ComboBoxEx32 = win32gui.FindWindowEx(
                    dialog, 0, 'ComboBoxEx32', None)  # 二级
                ComboBox = win32gui.FindWindowEx(
                    ComboBoxEx32, 0, 'ComboBox', None)  # 三级
                edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 四级
                button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 五级
                win32gui.SendMessage(edit, win32con.WM_SETTEXT,
                                     None, imgFile)  # 循环到最后一次退出上传框
                win32gui.SendMessage(dialog, win32con.WM_COMMAND,
                                     1, button)  # 循环到最后一次退出上传框
                if up_img not in img[len(img)-1]:
                    WebDriverWait(browser, 15).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul>li[class="add"]')))
                    browser.find_element_by_css_selector(
                        'ul>li[class="add"]').click()
            sleep(3)
            lg_total_key1 = '['+randString(lg_loc) + \
                randString(lg_disease)+randString(compose_key)+']'
            lg_total_key2 = '['+randString(lg_loc) + \
                randString(lg_disease)+randString(compose_key)+']'
            lg_total_key3 = '['+randString(lg_loc) + \
                randString(lg_disease)+randString(compose_key)+']'

            lg_content = lg_total_key1+lg_total_key2+'欢迎拨打下方咨询热线' + \
                lg_total_key+rand_str+lg_total_key3  # 动态调用

            browser.find_element_by_css_selector(
                ".input textarea[node-type='textEl']").send_keys(ra_content)
            browser.find_element_by_css_selector(
                ".func a[node-type='submit']").click()
            sleep(3)
            lg_post_time += 1
        logout()
    lg_account.pop()
    lg_account.pop()
    lg_account.pop()
    lg_account.pop()

browser.close()
