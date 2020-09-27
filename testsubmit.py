# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
import hashlib
import time
from tkinter import ttk
from tkinter import filedialog

class TestSubmitGUI():
    selectfileEntered=object

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.menu()

    #设置菜单
    def menu(self):
        # Creating a Menu Bar
        win=self.init_window_name
        menuBar = Menu(win)
        win.config(menu=menuBar)

        # Add menu items
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="新建")
        fileMenu.add_separator()
        fileMenu.add_command(label="退出")
        menuBar.add_cascade(label="文件", menu=fileMenu)
        # Add another Menu to the Menu Bar and an item
        msgMenu = Menu(menuBar, tearoff=0)
        msgMenu.add_command(label="通知 Box")
        msgMenu.add_command(label="警告 Box")
        msgMenu.add_command(label="错误 Box")
        msgMenu.add_separator()
        msgMenu.add_command(label="判断对话框")
        menuBar.add_cascade(label="消息框", menu=msgMenu)



    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("文本处理工具_v1.2")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.init_window_name)  # Create Tab Control
        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='单个测试')  # Add the tab
        tab2 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab2, text='批量测试')  # Make second tab visible

        # tabControl.pack(expand=1, fill="both")  # Pack to make visible
        tabControl.grid(column=0, row=0, padx=8, pady=4)
        # ~ Tab Control introduced here -----------------------------------------

        # ---------------Tab1控件------------------#
        # We are creating a container tab1 to hold all other widgets
        monty = ttk.LabelFrame(tab1, text='单个测试1')
        monty.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(monty, text="学号:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        student_name = tk.StringVar()
        studentnameEntered = ttk.Entry(monty, width=12, textvariable=student_name)
        studentnameEntered.grid(column=1, row=0, sticky='W')

        ttk.Label(monty, text="密码:").grid(column=2, row=0, sticky='W')
        # Adding a Textbox Entry widget
        student_pwd = tk.StringVar()
        studentpwdEntered = ttk.Entry(monty, width=12, textvariable=student_pwd)
        studentpwdEntered.grid(column=3, row=0, sticky='W')


        # ---------------Tab1控件------------------#
        # We are creating a container tab1 to hold all other widgets
        monty = ttk.LabelFrame(tab2, text='批量测试')
        monty.grid(column=0, row=0, padx=8, pady=4)
        ttk.Label(monty, text="选择导入文件:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        selectfile = tk.StringVar()
        self.selectfileEntered = ttk.Entry(monty, width=48, textvariable=selectfile)
        self.selectfileEntered.grid(column=1, row=0, sticky='W')
        button1 = ttk.Button(monty, text='浏览', width=8, command=self.selectExcelfile)
        button1.grid(column=2,row=0,sticky='W')

        btn_process = ttk.Button(monty, text='启动进度条', command=self.progress)
        btn_process.grid(column=3,row=0,sticky='W')

        # -----------------------------------------
        # -----------------------------------------
        proc_frame = ttk.Frame(self.init_window_name)
        # self.log_label.pack(expand=1, fill="both")
        # 设置下载进度条
        ttk.Label(proc_frame , text='处理进度:').grid(column=0,row=1,sticky='W')
        self.canvas = tk.Canvas(proc_frame, width=465, height=22, bg="white")
        self.canvas.grid(column=1,row=1,sticky='W')
        proc_frame.grid(column=0, row=1)

        # Using a scrolled Text control
        scrolW = 60;
        scrolH = 5
        scr = scrolledtext.ScrolledText(proc_frame, width=scrolW, height=scrolH, wrap=tk.WORD)
        scr.grid(column=0, row=2, sticky='WE', columnspan=3)




    # 显示下载进度
    def progress(self):
        # 填充进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数
        for i in range(x):
            n = n + 465 / x
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.init_window_name.update()
            time.sleep(0.02)  # 控制进度条流动的速度

        # 清空进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        x = 500  # 未知变量，可更改
        n = 465 / x  # 465是矩形填充满的次数

        for t in range(x):
            n = n + 465 / x
            # 以矩形的长度作为变量值更新
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.init_window_name.update()
            time.sleep(0)  # 时间为0，即飞速清空进度条

    #定义文件导入选择控件
    def selectExcelfile(self):
        sfname = filedialog.askopenfilename(title='选择Excel文件', filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])
        print(sfname)
        self.selectfileEntered.insert(INSERT,sfname)

    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")



def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = TestSubmitGUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()