import os
import re
import tkinter as tk

with open('./账号/ra_account.txt', 'r', encoding='utf-8-sig') as ra_account:  # 深圳账号
    shenzhen_account = ra_account.readlines()
sz_account = shenzhen_account
print(len(sz_account))
with open('./账号/lg_account.txt', 'r', encoding='utf-8-sig') as lg_account:  # 厦门账号
    lugang_account = lg_account.readlines()
xm_account = lugang_account
print(xm_account[-4])
# print(xm_account[1])
# print(xm_account[2])
# print(xm_account[3])
# print(xm_account[4])
# del xm_account[1]
# del xm_account[2]
# del xm_account[3]
# del xm_account[4]
# del xm_account[5]
# del xm_account[6]
# xm_account.pop()
# xm_account.pop(1)
# xm_account.pop(2)
if len(xm_account) % 4 == 0:
    print('yes')
else:
    print('no')
print(xm_account)
# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('错误')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上设定标签
l = tk.Label(window, text='你好！this is Tkinter', bg='pink',
             font=('Arial', 12), width=30, height=2)
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

# 第5步，放置标签
l.pack()    # Label内容content区域放置位置，自动调节尺寸
# 放置lable的方法有：1）l.pack(); 2)l.place();

# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
