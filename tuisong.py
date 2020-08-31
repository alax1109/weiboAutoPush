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

"""
@param int      total            文章发布次数
@param string   img_dir          图片路径
@param int      img[:limit]      图片发布数量
@param string   account_password 账号密码
@param int      xx_total_time    总共发布次数
"""

renai_path = './blog/weibo/renai_article/'
lugang_path = './blog/weibo/lugang_article/'
dongguang_path = './blog/weibo/dongguang_article/'

ra_files = os.listdir(renai_path)
lg_files = os.listdir(lugang_path)
# dg_files = os.listdir(dongguang_path)

ra_img_dir = './blog/weibo/renai_pic/'
ra_img_upload = os.listdir(ra_img_dir)
ra_img_upload.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
img = ra_img_upload[:9]

lg_img_dir = './blog/weibo/lugang_pic'
lg_img_upload = os.listdir(lg_img_dir)
lg_img_upload.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
img = lg_img_upload[:9]

# dg_img_dir = './blog/weibo/dongguang_pic'
# dg_img_upload = os.listdir(lg_img_dir)
# dg_img_upload.sort(key=lambda i: int(re.match(r'(\d+)', i).group()))
# img = dg_img_upload[:9]

main_dir = os.getcwd()

ra_upload_img_dir = '\\blog\\weibo\\renai_pic'
lg_upload_img_dir = '\\blog\\weibo\\lugang_pic'
dg_upload_img_dir = '\\blog\\weibo\\dongguang_pic'

ra_post_time = 0  # 仁爱发布次数
ra_total_time = 1  # 仁爱总发布次数
lg_post_time = 0  # 鹭港
lg_total_time = 1  # 鹭港总发布次数
dg_post_time = 0  # 东莞
dg_total_time = 1  # 东莞总发布次数

account_passwd = {
    'renai': {
        'account': '18903021908',
        'pwd': 'xmlgyy120'
    },
    'lugang': {
        'account': '15394468470',
        'pwd': 'xmlgyy120'
    }
}


browser = webdriver.Firefox()
browser.get('https://www.weibo.com/')
WebDriverWait(browser, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".info_list.login_btn a[node-type='submitBtn']")))


def login(username, password):
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


login(account_passwd['renai']['account'], account_passwd['renai']['pwd'])
sleep(8)
while WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                   ".func a[node-type='submit']"))) and ra_post_time <= ra_total_time:  # 文章发布次数
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
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 四级
        win32gui.SendMessage(edit, win32con.WM_SETTEXT,
                             None, imgFile)  # 循环到最后一次退出上传框
        win32gui.SendMessage(dialog, win32con.WM_COMMAND,
                             1, button)  # 循环到最后一次退出上传框
        if up_img not in img[len(img)-1]:
            WebDriverWait(browser, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul>li[class="add"]')))
            browser.find_element_by_css_selector(
                'ul>li[class="add"]').click()
    for file in ra_files:
        f = open(renai_path+file, encoding='utf8')  # 打开目录文件
        c = f.read()
        content = re.sub("<[^>]*?>", "", c)
        content = re.sub("湖里", "福田", c)
        content = re.sub("权威专家", "医师", c)
        content = re.sub("专家", "医师", c)
        content = re.sub("北京", "深圳", c)
        content = re.sub("人流", "深圳人流", c)
        content = re.sub("药流", "深圳药流", c)
        content = re.sub(
            r"http://www.fh21.com.cn/fuke/yc/rl/", r"http://www.ra120.cn/", c)
        content = content.strip("")
        f.close()
        del ra_files[0]
        dir_file_remove = renai_path + "/" + file  # 循环删除对应目录下文件
        os.remove(dir_file_remove)
        sleep(5)
        break
    browser.find_element_by_css_selector(
        ".input textarea[node-type='textEl']").send_keys(content)
    browser.find_element_by_css_selector(
        ".func a[node-type='submit']").click()
    sleep(3)
    ra_post_time += 1


logout()
login(account_passwd['lugang']['account'], account_passwd['lugang']['pwd'])
while WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                   ".func a[node-type='submit']"))) and lg_post_time <= lg_total_time:  # 文章发布次数
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
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 四级
        win32gui.SendMessage(edit, win32con.WM_SETTEXT,
                             None, imgFile)  # 循环到最后一次退出上传框
        win32gui.SendMessage(dialog, win32con.WM_COMMAND,
                             1, button)  # 循环到最后一次退出上传框
        if up_img not in img[len(img)-1]:
            WebDriverWait(browser, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul>li[class="add"]')))
            browser.find_element_by_css_selector(
                'ul>li[class="add"]').click()
    for file in lg_files:
        f = open(lugang_path+file, encoding='utf8')  # 打开目录文件
        c = f.read()
        content = re.sub("<[^>]*?>", "", c)
        # content = re.sub("湖里", "福田", c)
        content = re.sub("权威专家", "医师", c)
        content = re.sub("专家", "医师", c)
        content = re.sub("北京", "厦门", c)
        content = re.sub("药流", "厦门药流", c)
        content = re.sub("人流", "厦门人流", c)
        content = content.strip("")
        f.close()
        del lg_files[0]
        dir_file_remove = lugang_path + "/" + file  # 循环删除对应目录下文件
        os.remove(dir_file_remove)
        sleep(5)
        break
    browser.find_element_by_css_selector(
        ".input textarea[node-type='textEl']").send_keys(content)
    browser.find_element_by_css_selector(
        ".func a[node-type='submit']").click()
    sleep(3)
    lg_post_time += 1
browser.close()

# if __name__ == "__main__":
