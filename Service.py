# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import time
import requests
import json
import logging
import random
import ReadConfig

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='worksubmit.log', level=logging.INFO, format=LOG_FORMAT)
logging.basicConfig(filename='worksubmit_error.log', level=logging.ERROR, format=LOG_FORMAT)

class Service(object):
    #papernum=0  #试卷数
    #havesub_papernum=0 #已经提交的试卷数
    testSubmitGUI=None
    def __init__(self):
        self.headers={
            'Referer':'https://jxjyxb.bucm.edu.cn/stu.html',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Host':'jxjyxb.bucm.edu.cn'
        }
        self.login_url='https://jxjyxb.bucm.edu.cn/stu.html#/login'
        self.post_url='https://jxjyxb.bucm.edu.cn/api/v1/student/main/login'
        self.logined_url='https://jxjyxb.bucm.edu.cn/stu.html#/xuexi/benxueqi'
        self.session=requests.Session()

        self.config = ReadConfig.ReadConfig()




    def login(self,login_name,login_psw):
        post_data={
            'student.studentNo':login_name,
            'student.pwd':login_psw
        }
        response=self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code==200:
            userlogininfo=response.text
            print(userlogininfo)
            #logging.info(response.text)
            logininfo=json.loads(response.text)
            if logininfo is not None:
                if logininfo['code']==100:
                    # 学生名字
                    student_name=logininfo['stu']['name']
                    response=self.session.get(self.logined_url,headers=self.headers)
                    if response.status_code==200:
                        logstr='用户'+str(login_name)+'登录成功,学生姓名：'+student_name
                        self.log(logstr,True)
                        return logininfo
                else:
                    self.log('用户' + str(login_name) + "登录失败！",True)


    #获取学员选课信息
    def geteleactive(self,semeId,studentNo):
        #选课信息URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/eleactive/list'
        post_data={
            'page': '1',
            'pageSize': '100',
            'eleactive.semeId': semeId,
            'eleactive.studentNo': studentNo
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            #logging.info(response.text)
            self.log('获取学生'+str(studentNo)+'选课信息成功！')
            #print(response.text)
            eleactivedata=json.loads(response.text)
            if eleactivedata is not None:
                courselist=eleactivedata['pager']['datas']
                for course in courselist:
                    semeId=course['semeId']
                    courseId = course['courseId']
                    courseName = course['courseD']
                    self.log('获取学生'+str(studentNo)+'选课'+courseName+'成功！',True)
                    courseplanid =''
                    if 'coursePlanId' in course:
                        courseplanid=course['coursePlanId']
                    if self.getstudentlearninfo(courseplanid):
                        self.log('获取学生'+str(studentNo)+'选课'+courseName+'学习计划'+str(courseplanid)+'成功',True)
                        self.getstudentcursework(login_name=studentNo,semeId=semeId,courseId=courseId,courseName=courseName)
                    else:
                        self.log('获取学生' + str(studentNo) + '选课' + courseName + '学习计划' + str(courseplanid) + '失败',True)

    # 获取学生学习计划
    def getstudentlearninfo(self,coursePlanId):
        iflearn=False
        # 作业列表URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/courseplan/learninfo?coursePlanId='+str(coursePlanId)
        response = self.session.get(request_url,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            if response.text is not None and response.text!='':
                result_data = json.loads(response.text)
                if result_data is not None:
                    if result_data['code']==100:
                        iflearn=True
        return iflearn

    # 获取学生作业
    def getstudentcursework(self,login_name,semeId,courseId,courseName):
        #作业列表URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_list'
        post_data={
            'semeId':semeId,
            'courseId':courseId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            #logging.info(response.text)
            paperdata=json.loads(response.text)
            if paperdata is not None:
                papernum=len(paperdata)
                havesub_papernum=0
                #self.show_singstudent_proc(maximum=papernum,value=havesub_papernum)
                self.log('获取学生'+str(login_name)+courseName+'作业信息成功！共'+str(papernum)+'套作业',True)
                for paper in paperdata:
                    workId=paper['id']
                    paperId=paper['paperId']
                    paperName=paper['name']
                    createTimeStr=paper['createTime']
                    createTimeArray = time.localtime(createTimeStr / 1000)
                    createTime = time.strftime("%Y-%m-%d %H:%M:%S", createTimeArray)

                    endTimeStr=paper['endTime']
                    endTimeArray = time.localtime(endTimeStr / 1000)
                    endTime = time.strftime("%Y-%m-%d %H:%M:%S", endTimeArray)

                    timeStamp = time.time()  # 1559286774.2953627
                    timeArray = time.localtime(timeStamp)
                    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

                    #print('创建时间' + createTime)
                    #print('结束时间' + endTime)
                    #print('当前时间' + currentTime)
                    havesub_papernum += 1
                    if currentTime > createTime and currentTime < endTime:
                        if 'courseWorkStu' in paper:
                            courseWorkcreateTime=paper['courseWorkStu']['createTime']
                            print(createTime)
                            timeArray= time.localtime(courseWorkcreateTime/1000)
                            workTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                            self.log('学生'+str(login_name)+'第' + str(havesub_papernum) + '套作业-试卷编号：' + str(paperId) + '-' + paperName+'在'+workTime+'提交过！',True)
                            #self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                        else:
                            self.getstudentpaper(login_name=login_name,paperId=paperId,paperName=paperName,workId=workId)
                            self.log('学生'+str(login_name)+'自动完成第' + str(havesub_papernum) + '套作业-试卷编号：'+str(paperId)+'-'+paperName,True)
                            #self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                            workdelaytime=self.getworkdelaytime()
                            self.log('休息'+str(workdelaytime)+'秒....',False)
                            time.sleep(workdelaytime)
                    else:
                        self.log('学生' + str(login_name) + '第' + str(havesub_papernum) + '套作业-试卷编号：' + str(
                            paperId) + '-' + paperName + '没有在作业时间范围之内,暂不能开始作业！', True)



    # 获取试卷
    def getstudentpaper(self,login_name,paperId,paperName,workId):
        #试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/paper'
        paperId=paperId
        post_data={
            'paperId':paperId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            paperinfo=json.loads(response.text)
            itemnum=len(paperinfo)
            havdo_itemnum=0
            self.log('学生'+str(login_name)+'试卷'+paperName+'('+str(paperId)+')共'+str(itemnum)+'道题目')
            self.set_status('学生'+str(login_name)+'正在进行试卷' + str(paperId) + '-'+paperName+'， 共' + str(itemnum) + '道题目。')
            self.show_dowork_proc(maximum=itemnum, value=havdo_itemnum)
            itemdelaytime =self.get_itemdelaytime()
            for queitem in paperinfo:
                print(queitem['id'])
                self.log('学生'+str(login_name)+'正在准备题号'+str(queitem['id'])+'的答案')
                if 'quelib' in queitem:
                    type = queitem['quelib']['type'] #
                    if type==0 or type==2:
                        if 'ok1' in queitem['quelib']:
                            queitem['quelib']['okFlag']=queitem['quelib']['ok1']
                            self.log('答案为'+queitem['quelib']['okFlag'])
                    if type == 1:
                        #queitem['quelib']['okFlag'] = queitem['quelib']['ok1']
                        for num in range(1,10):
                            ok = 'ok'+str(num)
                            if ok in queitem['quelib']:
                                okflag = 'okFlag'
                                if num > 1:
                                    okflag='okFlag'+str(num)
                                queitem['quelib'][okflag] = queitem['quelib'][ok]
                                self.log('答案为' + queitem['quelib'][okflag])
                    if type == 3:
                        print('问答题')
                havdo_itemnum += 1
                itemdelaytime = self.get_itemdelaytime()
                print('答案准备时间：'+str(itemdelaytime))
                time.sleep(itemdelaytime)
                self.show_dowork_proc(maximum=itemnum, value=havdo_itemnum)
            subpaper=json.dumps(paperinfo,ensure_ascii=False)
            print(subpaper)
            #提交试卷
            time.sleep(itemdelaytime)
            self.submitpaper(login_name=login_name,paperId=paperId,workId=workId,subpaper=subpaper)

    def getstudentworktest(self,paperId):
        # 试卷URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_test'
        post_data = {
            'paperId': paperId
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('test---'+response.text)

    # 提交试卷
    def submitpaper(self,login_name,paperId,workId,subpaper):
        # 提交试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/submit_work?paperId='+str(paperId)+'&workId='+str(workId)
        post_data={
            'sub':subpaper
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('submit paper---'+response.text)
            self.log('学生'+str(login_name)+'自动提交试卷：' + response.text,True)

    # 显示单个学生的作业进度
    def show_dowork_proc(self,maximum,value):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.show_procbar_process(maximum,value)

    # 显示具体的进度信息
    def inserttolog(self,str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.insertToLog(str)
    # 记日志
    def log(self,logstr,islog=False):
        self.inserttolog(logstr)
        if islog:
            logging.info(logstr)

    def get_itemdelaytime(self):
        itemdelaytime = random.randint(1, 3)  # 等待时间
        configdelaytime=self.getconfigdelaytime('delay-time','itemdelay')
        if configdelaytime>0:
            itemdelaytime=configdelaytime
        return itemdelaytime


    def getworkdelaytime(self):
        workdelaytime = random.randint(10, 20)  # 等待时间
        configdelaytime = self.getconfigdelaytime('delay-time', 'workdelay')
        if configdelaytime > 0:
            workdelaytime = configdelaytime
        return workdelaytime

    def getconfigdelaytime(self,option,item):
        delaytime=0
        if self.config.get_configvalue(option, item):
            delayconf = self.config.get_configvalue(option, item)
            delayarry = delayconf.split(',')
            if len(delayarry) == 2:
                delaytime = random.randint(int(delayarry[0]), int(delayarry[1]))
        return delaytime


    # 设置状态栏的状态信息
    def set_status(self,str):
        if self.testSubmitGUI is not None:
            self.testSubmitGUI.set_status_bar(str)

if __name__=='__main__':
    service=Service()
    service.login(login_name='201820113109',login_psw='806854137')
    #service.geteleactive(semeId='40',studentNo='202020121200')
    #service.getstudentpaper(1002,1107)
    service.getstudentpaper('201820113109','684','医古文B',684)
    #print(service.getstudentlearninfo('46903'))