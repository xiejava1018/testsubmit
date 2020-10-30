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
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
import Service
import time
import xlrd
import _thread



class TestSubmitGUI():
    selectfileEntered=object

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        #self.menu()
        # 初始化服务
        self.service = Service.Service()

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
        fileMenu.add_command(label="退出", command=_quit)
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
        self.init_window_name.title("自动作业工具_v0.9beta")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('600x480+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.init_window_name)  # Create Tab Control
        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='单用户作业')  # Add the tab
        tab2 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab2, text='批量用户作业')  # Make second tab visible
        tab3 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab3, text='自动选课')  # Make second tab visible

        # tabControl.pack(expand=1, fill="both")  # Pack to make visible
        tabControl.grid(column=0, row=0, padx=8, pady=4)
        # ~ Tab Control introduced here -----------------------------------------

        # ---------------Tab1控件------------------#
        # We are creating a container tab1 to hold all other widgets
        ttk.Label(tab1, text="学号:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        self.student_name = tk.StringVar()
        self.studentnameEntered = ttk.Entry(tab1, width=20, textvariable=self.student_name)
        self.student_name.set(r'202020121200')
        self.studentnameEntered.grid(column=1, row=0, sticky='W')

        ttk.Label(tab1, text="密码:").grid(column=2, row=0, sticky='W')
        # Adding a Textbox Entry widget
        self.student_pwd = tk.StringVar()
        self.studentpwdEntered = ttk.Entry(tab1, show='*',width=20, textvariable=self.student_pwd)
        self.student_pwd.set(r'1qaz2wsx')
        self.studentpwdEntered.grid(column=3, row=0, sticky='W')

        btn_process_single = ttk.Button(tab1, text='启动自动测试', command=self.procsingletest)
        btn_process_single.grid(column=4, row=0, sticky='W')


        # ---------------Tab2控件------------------
        ttk.Label(tab2, text="选择导入文件:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        selectfile = tk.StringVar()
        self.selectfileEntered = ttk.Entry(tab2, width=48, textvariable=selectfile)
        self.selectfileEntered.grid(column=1, row=0, sticky='W')
        button1 = ttk.Button(tab2, text='浏览', width=8, command=self.selectExcelfile)
        button1.grid(column=2,row=0,sticky='W')

        btn_process_batch = ttk.Button(tab2, text='启动自动测试', command=self.procbatchtest)
        btn_process_batch.grid(column=3, row=0, sticky='W')

        # ----------------Tab3控件-------------------
        ttk.Label(tab3, text="选择导入文件:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        selectfile = tk.StringVar()
        self.selectfileEntered = ttk.Entry(tab3, width=48, textvariable=selectfile)
        self.selectfileEntered.grid(column=1, row=0, sticky='W')
        button1 = ttk.Button(tab3, text='浏览', width=8, command=self.selectExcelfile)
        button1.grid(column=2,row=0,sticky='W')

        btn_pro_selcourse = ttk.Button(tab3, text='启动自动选课', command=self.procbatchtest)
        btn_pro_selcourse.grid(column=3, row=0, sticky='W')


        # ----------------进度条-----------------------
        self.proc_frame = ttk.LabelFrame(self.init_window_name, text="进度信息", relief=SUNKEN)

        self.progressbar = ttk.Progressbar(self.proc_frame, length=560, mode='determinate', orient=HORIZONTAL)
        self.progressbar.grid(row=0, column=0)
        self.proc_frame.grid(column=0, row=1)

        # ----------------滚动文本框----------------
        scrolW = 80;
        scrolH = 25;
        self.logscr = scrolledtext.ScrolledText(self.proc_frame, width=scrolW, height=scrolH, wrap=tk.WORD)
        self.logscr.grid(column=0, row=2, pady=10,sticky='WE', columnspan=10)

        # ----------------状态栏-------------------
        self.statuslabel = ttk.Label(self.init_window_name,textvariable=status,width=83,anchor=W)
        self.statuslabel.grid(column=0, row=2, padx=5,pady=2,sticky='W')

    def show_progress(self):
        self.progressbar["maximum"] = 100
        self.progressbar["value"] = 0
        for i in range(100):
            self.progressbar["value"] = i + 1
            self.proc_frame.update()
            time.sleep(0.1)

    # 自动处理单个学生的作业
    def procsingletest(self):
        self.init_proc()
        studentname = self.studentnameEntered.get()
        studentpwd = self.studentpwdEntered.get()
        #self.procdowork(studentname,studentpwd)
        try:
            _thread.start_new_thread(self.dosingework, (studentname, studentpwd,))

        except:
            print("Error: 无法启动线程")
            self.service.log('Error: 无法启动线程', True)

    # 做单个作业
    def dosingework(self,stud_no,stud_pwd):
        self.procdowork(stud_no,stud_pwd)
        self.service.log(str(stud_no)+'自动作业执行完成！', True)
        self.set_status_bar(str(stud_no)+'自动作业执行完成！')

    # 自动批量处理学生作业
    def procbatchtest(self):
        self.init_proc()
        # 读取excel文件
        book = xlrd.open_workbook(self.selectfileEntered.get())
        sheet1 = book.sheets()[0]
        try:
            _thread.start_new_thread(self.dobatch, (sheet1,))
        except:
            print("Error:无法启动线程")
            self.service.log('Error: 无法启动线程', True)

    # 批量处理作业
    def dobatch(self,sheet1):
        nrows = sheet1.nrows
        for row in range(nrows):
            row_values = sheet1.row_values(row)
            studentname = row_values[1]
            studentpwd = row_values[2]
            self.procdowork(studentname, studentpwd)
        self.service.log('批量自动作业执行完成！', True)
        self.set_status_bar('批量自动作业执行完成！')

    # 自动作业
    def procdowork(self,studentNo,studentpwd):
        loginuser=self.service.login(login_name=studentNo,login_psw=studentpwd)
        if loginuser is not None:
            xueqiid=loginuser['stu']['xueqi']['id']  # 学生学期
            self.service.geteleactive(semeId=xueqiid,studentNo=studentNo)
        else:
            print(str(loginuser)+'登录失败')

    # 初始化进度条和日志显示栏
    def init_proc(self):
        #self.service.papernum=0
        #self.service.havesub_papernum=0
        self.progressbar["maximum"] = 0
        self.progressbar["value"] = 0
        self.proc_frame.update()
        self.logscr.delete(0.0, END)

    # 插入显示日志
    def insertToLog(self, str):
        self.logscr.insert(INSERT, str+'\n')
        self.logscr.see(END)

    # 进度条
    def show_procbar_process(self, maximum, value):
        self.progressbar["maximum"] = maximum
        self.progressbar["value"] = value
        self.proc_frame.update()

    # 状态栏
    def set_status_bar(self,status_msg):
        status.set(status_msg)

    #定义文件导入选择控件
    def selectExcelfile(self):
        sfname = filedialog.askopenfilename(title='选择Excel文件', filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])
        print(sfname)
        self.selectfileEntered.insert(INSERT,sfname)

# Exit GUI cleanly
def _quit():
    init_window.quit()
    init_window.destroy()
    exit()

init_window = Tk()
status = StringVar()
status.set('状态:')
def gui_start():
    #实例化出一个父窗口
    testsubmitGUI = TestSubmitGUI(init_window)
    # 设置根窗口默认属性
    testsubmitGUI.set_init_window()
    testsubmitGUI.service.testSubmitGUI=testsubmitGUI

    init_window.mainloop()


gui_start()