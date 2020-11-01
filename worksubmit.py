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
import UtilTools
import ReadConfig

class TestSubmitGUI():
    selectfileEntered=object

    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.menu()
        # 读配置文件
        self.config = ReadConfig.ReadConfig()
        # 初始化服务
        self.service = Service.Service()
        self.utiltools=UtilTools.UtilTools()


    #设置菜单
    def menu(self):
        # Creating a Menu Bar
        win=self.init_window_name
        menuBar = Menu(win)
        win.config(menu=menuBar)

        # Add menu items
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="刷新自定义作业数据", command=self.refresh_selectwork)
        fileMenu.add_command(label="刷新推荐选课数据", command=self.refresh_selectcourse)
        fileMenu.add_separator()
        fileMenu.add_command(label="导入自定义作业数据", command=self.load_selectwork)
        fileMenu.add_command(label="导入推荐选课数据", command=self.load_selectcourse)
        fileMenu.add_separator()
        fileMenu.add_command(label="退出", command=_quit)
        menuBar.add_cascade(label="加载初始化数据", menu=fileMenu)
        # Add another Menu to the Menu Bar and an item
        #msgMenu = Menu(menuBar, tearoff=0)
        #msgMenu.add_command(label="通知 Box")
        #msgMenu.add_command(label="警告 Box")
        #msgMenu.add_command(label="错误 Box")
        #msgMenu.add_separator()
        #msgMenu.add_command(label="判断对话框")
        #menuBar.add_cascade(label="消息框", menu=msgMenu)



    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("自动作业工具_v1.0")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('600x480+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.init_window_name)  # Create Tab Control
        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='单用户操作')  # Add the tab
        tab2 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab2, text='批量用户操作')  # Make second tab visible
        #tab3 = ttk.Frame(tabControl)  # Add a second tab
        #tabControl.add(tab3, text='自动选课')  # Make second tab visible

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

        btn_process_single = ttk.Button(tab1, text='自动作业', command=self.procsingletest)
        btn_process_single.grid(column=4, row=0, sticky='W')
        btn_proc_selcourse_single = ttk.Button(tab1, text='自动选课', command=self.procsingle_selectcourse)
        btn_proc_selcourse_single.grid(column=5, row=0, sticky='W')


        # ---------------Tab2控件------------------
        ttk.Label(tab2, text="导入文件:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        self.selectfile = tk.StringVar()
        self.selectfileEntered = ttk.Entry(tab2, width=40, textvariable=self.selectfile)
        self.selectfileEntered.grid(column=1, row=0, sticky='W')
        button1 = ttk.Button(tab2, text='浏览...', width=8, command=self.selectExcelfile)
        button1.grid(column=2,row=0,sticky='W')

        btn_process_batch = ttk.Button(tab2, text='自动作业', command=self.procbatchtest)
        btn_process_batch.grid(column=3, row=0, sticky='W')
        btn_proc_selcourse_batch = ttk.Button(tab2, text='自动选课', command=self.procbatch_selectcourse)
        btn_proc_selcourse_batch.grid(column=4, row=0, sticky='W')

        # ----------------Tab3控件-------------------
        #ttk.Label(tab3, text="选择导入文件:").grid(column=0, row=0, sticky='W')
        # Adding a Textbox Entry widget
        #selectfile = tk.StringVar()
        #self.selectfileEntered = ttk.Entry(tab3, width=48, textvariable=selectfile)
        #self.selectfileEntered.grid(column=1, row=0, sticky='W')
        #button1 = ttk.Button(tab3, text='浏览', width=8, command=self.selectExcelfile)
        #button1.grid(column=2,row=0,sticky='W')

        #btn_pro_selcourse = ttk.Button(tab3, text='启动自动选课', command=self.procbatchtest)
        #btn_pro_selcourse.grid(column=3, row=0, sticky='W')


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

    # 自动处理单个学生选课
    def procsingle_selectcourse(self):
        self.init_proc()
        studentname = self.studentnameEntered.get()
        studentpwd = self.studentpwdEntered.get()
        try:
            _thread.start_new_thread(self.service.student_selectcourse, (studentname, studentpwd,))
            self.set_status_bar(str(studentname)+'自动选课执行完成！')
        except:
            print("Error: 无法启动线程")
            self.service.log('Error: 无法启动线程', True)

    def procbatch_selectcourse(self):
        self.init_proc()
        # 读取excel文件
        if self.selectfileEntered.get():
            book = xlrd.open_workbook(self.selectfileEntered.get())
            sheet1 = book.sheets()[0]
            try:
                _thread.start_new_thread(self.dobatch_selectcourse, (sheet1,))
            except:
                print("Error:无法启动线程")
                self.service.log('Error: 无法启动线程', True)
        else:
            self.service.log('请导入文件！')

    # 批量处理选课
    def dobatch_selectcourse(self,sheet1):
        nrows = sheet1.nrows
        maximum=nrows
        i=0
        self.show_procbar_process(maximum,i)
        indexrow_values=sheet1.row_values(0)
        if '学号' in indexrow_values and '密码' in indexrow_values:
            index_stuno=indexrow_values.index('学号')
            index_stupwd=indexrow_values.index('密码')
            for row in range(1,nrows):
                row_values = sheet1.row_values(row)
                studentname = row_values[index_stuno]
                studentpwd = row_values[index_stupwd]
                self.service.student_selectcourse(studentname, studentpwd)
                i = i + 1
                self.show_procbar_process(maximum, i)
            self.show_procbar_process(0, 0)
            self.service.log('批量选课执行完成！', True)
            self.set_status_bar('批量选课执行完成！')
        else:
            self.service.log('请确认导入文件格式是否正确！')

    # 做单个作业
    def dosingework(self,stud_no,stud_pwd):
        self.procdowork(stud_no,stud_pwd)
        self.service.log(str(stud_no)+'自动作业执行完成！', True)
        self.set_status_bar(str(stud_no)+'自动作业执行完成！')

    # 自动批量处理学生作业
    def procbatchtest(self):
        self.init_proc()
        # 读取excel文件
        if self.selectfileEntered.get():
            book = xlrd.open_workbook(self.selectfileEntered.get())
            sheet1 = book.sheets()[0]
            try:
                _thread.start_new_thread(self.dobatch, (sheet1,))
            except:
                print("Error:无法启动线程")
                self.service.log('Error: 无法启动线程', True)
        else:
            self.service.log('请导入文件！')

    # 批量处理作业
    def dobatch(self,sheet1):
        nrows = sheet1.nrows
        maximum=nrows
        i=0
        self.show_procbar_process(maximum, i)
        indexrow_values = sheet1.row_values(0)
        if '学号' in indexrow_values and '密码' in indexrow_values:
            index_stuno = indexrow_values.index('学号')
            index_stupwd = indexrow_values.index('密码')
            for row in range(1,nrows):
                row_values = sheet1.row_values(row)
                studentname = row_values[index_stuno]
                studentpwd = row_values[index_stupwd]
                self.procdowork(studentname, studentpwd)
                i = i + 1
                self.show_procbar_process(maximum, i)
            self.show_procbar_process(0, 0)
            self.service.log('批量自动作业执行完成！', True)
            self.set_status_bar('批量自动作业执行完成！')
        else:
            self.service.log('请确认导入文件格式是否正确！')

    # 自动作业
    def procdowork(self,studentNo,studentpwd):
        loginuser=self.service.login(login_name=studentNo,login_psw=studentpwd)
        if loginuser is not None:
            xueqiid=loginuser['stu']['xueqi']['id']  # 学生学期
            self.service.geteleactive(semeId=xueqiid,studentNo=studentNo)
        else:
            print(str(loginuser)+'登录失败')

    # 定义文件导入选择控件
    def selectExcelfile(self):
        self.selectfile.set('')
        sfname = filedialog.askopenfilename(title='选择Excel文件', filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])
        print(sfname)
        self.selectfileEntered.insert(INSERT, sfname)

    # 刷新自定义作业初始化数据
    def refresh_selectwork(self):
        self.service.log('刷新自定义作业初始化数据', True)
        try:
            _thread.start_new_thread(self.service.init_selectworkdata, ())
        except:
            print("Error: 无法启动线程")
            self.service.log('Error: 无法启动线程', True)

    # 刷新选课初始化数据
    def refresh_selectcourse(self):
        self.service.log('刷新推荐选课初始化数据', True)
        try:
            _thread.start_new_thread(self.service.init_selectcoursedata, ())
        except:
            print("Error: 无法启动线程")
            self.service.log('Error: 无法启动线程', True)

    def load_selectwork(self):
        selectwork_fname = filedialog.askopenfilename(title='选择Excel文件', filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])
        if selectwork_fname:
            print(selectwork_fname)
            self.service.log('加载自定义作业数据文件'+selectwork_fname, True)
            try:
                _thread.start_new_thread(self.service.init_selectworkdata, (selectwork_fname,))
            except:
                print("Error: 无法启动线程")
                self.service.log('Error: 无法启动线程', True)


    def load_selectcourse(self):
        selectcourse_fname = filedialog.askopenfilename(title='选择Excel文件',filetypes=[('Excel', '*.xlsx'), ('All Files', '*')])
        if selectcourse_fname:
            print(selectcourse_fname)
            self.service.log('加载推荐选课数据文件' + selectcourse_fname, True)
            try:
                _thread.start_new_thread(self.service.init_selectcoursedata, (selectcourse_fname,))
            except:
                print("Error: 无法启动线程")
                self.service.log('Error: 无法启动线程', True)


    # 初始化进度条和日志显示栏
    def init_proc(self):
        #self.service.papernum=0
        #self.service.havesub_papernum=0
        self.progressbar["maximum"] = 0
        self.progressbar["value"] = 0
        self.proc_frame.update()
        self.logscr.delete(0.0, END)

    # 初始化数据
    def do_init_data(self):
        # 根据配置文件判断是否需要自动初始化数据
        autoloaddata = self.config.get_configvalue('setting', 'autoloaddata')
        if 'True'==autoloaddata:
            try:
                _thread.start_new_thread(self.auto_init_data,())
            except:
                print("Error: 无法启动线程")
                self.service.log('Error: 无法启动线程', True)

    def auto_init_data(self):
        if self.service.check_selectwork_ishaveinitdata()==False:
            self.service.init_selectworkdata()
        if self.service.check_selectcourse_ishaveinitdata()==False:
            self.service.init_selectcoursedata()
        self.set_status_bar('初始化数据成功！')


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
    testsubmitGUI.utiltools.testSubmitGUI=testsubmitGUI
    testsubmitGUI.service.set_utiltools(testsubmitGUI.utiltools)
    testsubmitGUI.do_init_data()
    init_window.mainloop()



gui_start()