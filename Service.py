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
import SelectWorkService
import DateUtil
import copy
import re
import SelectCourse

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='worksubmit.log', level=logging.INFO, format=LOG_FORMAT)
logging.basicConfig(filename='worksubmit_error.log', level=logging.ERROR, format=LOG_FORMAT)
neterror_msg='网络连接失败，请检查服务或网络是否正常！'

class Service(object):
    #papernum=0  #试卷数
    #havesub_papernum=0 #已经提交的试卷数
    testSubmitGUI=None
    utiltools=None
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
        # 读配置文件
        self.config = ReadConfig.ReadConfig()
        # 初始化学生选做作业信息
        self.selectworkService=SelectWorkService.SelectWorkService()
        self.selectworkService.utiltools=self.utiltools
        self.selectCourseService=SelectCourse.SelectCourseService()
        self.selectCourseService.utiltools = self.utiltools

    def set_utiltools(self,utiltools):
        self.utiltools=utiltools
        self.selectworkService.utiltools = self.utiltools
        self.selectCourseService.utiltools = self.utiltools

    # 登录
    def login(self,login_name,login_psw):
        post_data={
            'student.studentNo':login_name,
            'student.pwd':login_psw
        }
        try:
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
        except :
            self.log(neterror_msg, True)
            exit()



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
        try:
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
        except :
            self.log(neterror_msg, True)

    # 获取学生学习计划
    def getstudentlearninfo(self,coursePlanId):
        iflearn=False
        # 作业列表URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/courseplan/learninfo?coursePlanId='+str(coursePlanId)
        try:
            response = self.session.get(request_url,headers=self.headers)
            if response.status_code == 200:
                print(response.text)
                if response.text is not None and response.text!='':
                    result_data = json.loads(response.text)
                    if result_data is not None:
                        if result_data['code']==100:
                            iflearn=True
        except :
            self.log(neterror_msg, True)
        return iflearn

    # 获取学生作业
    def getstudentcursework(self,login_name,semeId,courseId,courseName):
        #作业列表URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_list'
        post_data={
            'semeId':semeId,
            'courseId':courseId
        }
        try:
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
                    # 判断是否是学生选做
                    isselectdo=self.selectworkService.isselectdo(login_name)
                    if isselectdo:
                        self.log('学生'+str(login_name) + '有要求选择性自动作业',True)
                    checkcourse='courseId='+str(courseId)
                    isdocourse=self.selectworkService.isdowork(str(login_name),checkcourse)
                    if isdocourse:
                        self.log('学生' +str(login_name) + '要求自动做' + checkcourse+'课程：'+courseName, True)
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
                                timeArray= time.localtime(courseWorkcreateTime/1000)
                                workTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                self.log('学生'+str(login_name)+'第' + str(havesub_papernum) + '套作业-试卷编号：' + str(paperId) + '-' + paperName+'在'+workTime+'提交过！',True)
                                #self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                            else:
                                checkwork='paperId='+str(paperId)+'&workId='+str(workId)
                                isdowork=self.selectworkService.isdowork(str(login_name),checkwork)
                                if isdowork:
                                    self.log('学生' + str(login_name) + '要求自动做' + checkwork + '作业：' + paperName, True)
                                if isselectdo==False or (isselectdo and isdocourse) or (isselectdo and isdowork):
                                    self.getstudentpaper(login_name=login_name,paperId=paperId,paperName=paperName,workId=workId)
                                    self.log('学生'+str(login_name)+'自动完成第' + str(havesub_papernum) + '套作业-试卷编号：'+str(paperId)+'-'+paperName,True)
                                    #self.show_singstudent_proc(maximum=papernum, value=havesub_papernum)
                                    workdelaytime=self.getworkdelaytime()
                                    self.log('休息'+str(workdelaytime)+'秒....',False)
                                    time.sleep(workdelaytime)
                        else:
                            self.log('学生' + str(login_name) + '第' + str(havesub_papernum) + '套作业-试卷编号：' + str(
                                paperId) + '-' + paperName + '没有在作业时间范围之内,暂不能开始作业！', True)
        except :
            self.log(neterror_msg, True)
            exit()



    # 获取试卷
    def getstudentpaper(self,login_name,paperId,paperName,workId):
        #试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/paper'
        paperId=paperId
        post_data={
            'paperId':paperId
        }
        try:
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
        except :
            self.log(neterror_msg, True)

    def getstudentworktest(self,paperId):
        # 试卷URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_test'
        post_data = {
            'paperId': paperId
        }
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                print('test---'+response.text)
        except :
            self.log(neterror_msg, True)

    # 提交试卷
    def submitpaper(self,login_name,paperId,workId,subpaper):
        # 提交试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/submit_work?paperId='+str(paperId)+'&workId='+str(workId)
        post_data={
            'sub':subpaper
        }
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                print('submit paper---'+response.text)
                self.log('学生'+str(login_name)+'自动提交作业：' + response.text,True)
        except :
            self.log(neterror_msg, True)


    # 学生选课
    def student_selectcourse(self,login_name,login_pwd):
        self.set_status(str(login_name) + '开始自动选课...')
        studinfo = self.login(login_name, login_pwd)
        if studinfo:
            self.stu_selectcourse(studinfo)
        self.set_status(str(login_name) + '自动选课执行完成！')

    def stu_selectcourse(self,studinfo,xuanke_counter=0):
        studenetId= studinfo['stu']['id']
        studentNo=studinfo['stu']['studentNo']
        semeId=str(int(studinfo['stu']['xueqi']['id'])+1) #本学期选下学期的课
        stu_plan_name = studinfo['stu']['planObj']['name']
        dateutil = DateUtil.DateUtil()
        semenum = dateutil.getSCTermNo(stu_plan_name)
        tobeelectlistinfo=self.get_stu_tobeelect(studinfo)
        if tobeelectlistinfo and len(tobeelectlistinfo)==2:
            stu_cur_eleactive=tobeelectlistinfo[0]
            tobeelectlist = tobeelectlistinfo[1]
            if stu_cur_eleactive and len(stu_cur_eleactive)>0 and self.getifforceselectcourse()!=True:
                self.log('学生' + str(studentNo) + '已有选课记录，不再进行自动选课。', True)
            else:
                # 优选本学期的推荐课,判断是否为推荐选课
                tobeelectlist = self.selectCourseService.get_recommend_courselist(studentNo)
                if xuanke_counter>0:
                    # 在所有推荐选课列表中先选主修课再选选修课
                    mainstudy_courselist=self.selectCourseService.get_recommend_courselist(studentNo,0)
                    if len(mainstudy_courselist)>=xuanke_counter:
                        tobeelectlist=mainstudy_courselist[0:xuanke_counter]
                    else:
                        selectstudy_courselist=self.selectCourseService.get_recommend_courselist(studentNo,1)
                        selectstudy_coursecount=len(selectstudy_courselist)
                        if selectstudy_coursecount>0:
                            selectstudycount=xuanke_counter-len(mainstudy_courselist)
                            if selectstudycount>selectstudy_coursecount:
                                selectstudycount=selectstudy_coursecount
                                mainstudy_courselist.extend(selectstudy_courselist[0:selectstudycount])
                            tobeelectlist =mainstudy_courselist
                # 组织自动选课数据
                selectcourselist = []
                for course in tobeelectlist:
                    # 优选本学期的推荐课,判断是否为推荐选课，如果是则选择
                    courseid = course['courseId']
                    coursetype = '必修'
                    if course['type'] == 0:
                        coursetype = '必修'
                    if course['type'] == 1:
                        coursetype = '选修'
                    selectcouse = {"coursePlanId": course['id'], "courseD": course['courseD'],
                                   "studentId": studenetId, "studentNo": studentNo,
                                   "courseId": courseid, "planId": course['planId'], "semeId": semeId,
                                   "type": coursetype, "time": "2020-10-31 12:41:41"}
                    selectcourselist.append(selectcouse)
                selectcourse_data=json.dumps(selectcourselist,ensure_ascii=False)
                self.submit_selectcourse(studinfo,selectcourse_data)

    def checkhavesamecourse(self,selectcourselist,courseid):
        for selectcouse in selectcourselist:
            if selectcouse['courseId']==courseid:
                return True
        return False


    # 提交选课信息
    def submit_selectcourse(self,studinfo,selectcourselist):
        studentNo = studinfo['stu']['studentNo']
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/eleactive/save2'
        post_data = {
            'eArr':selectcourselist
        }
        print(post_data)
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                print('选课' + response.text)
                xuanke_json = json.loads(response.text)
                xuanke_returncode = xuanke_json['code']
                xuanke_returnmsg=xuanke_json['msg']
                if 100==xuanke_returncode:
                    for selectcourse in json.loads(selectcourselist):
                        print(selectcourse)
                        self.log('学生' + str(studentNo) + '本次选课：' + selectcourse['courseD'], True)
                    self.log('学生' + str(studentNo) + '自动选课成功！', True)
                else:
                    self.log('学生' + str(studentNo) + '自动选课失败！'+xuanke_returnmsg, True)
                    if xuanke_returncode==0:
                        if '请选择课程' in xuanke_returnmsg:
                            self.log('请检查是否导入推荐选课数据，请初始化推荐选课数据后开始重新选课', False)
                        if '选课门数过多' in xuanke_returnmsg:
                            xuanke_counters=re.findall(r'\d+', xuanke_returnmsg)
                            if len(xuanke_counters)>0 and int(xuanke_counters[0])>0:
                                xuanke_counter=int(xuanke_counters[0])
                                self.log('学生' + str(studentNo) + '开始重新选课', True)
                                self.stu_selectcourse(studinfo,xuanke_counter)
                # 删除选课记录
                self.selectCourseService.delete_selctcourse(studentNo)
        except:
            self.log(neterror_msg, True)

    # 获取毕业条件
    def get_biyetiaojian(self):
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/main/biye_tiaojian'
        post_data = {
        }
        try:
            response = self.session.post(request_url,data=post_data,headers=self.headers)
            if response.status_code == 200:
                print('毕业条件---' + response.text)
                biyetiaojian_json = json.loads(response.text)
                bixiu_msg = biyetiaojian_json['bixiu_msg']
                xuanxiu_msg= biyetiaojian_json['xuanxiu_msg']
                bixiu_score=re.findall(r'\d+',bixiu_msg)
                xuanxiu_score=re.findall(r'\d+',xuanxiu_msg)
                print(bixiu_score)
                print(xuanxiu_score)
        except:
            self.log(neterror_msg, True)


    # 获取待选课列表
    def get_stu_tobeelect(self,student):
        if student:
            stu_No=student['stu']['studentNo']
            stu_plan_name = student['stu']['planObj']['name']
            stu_plan_level = student['stu']['planObj']['levelId']
            stu_plan_spec = student['stu']['planObj']['spec']
            stu_plan_id = student['stu']['planObj']['id']
            semeId=student['stu']['xueqi']['id']
            stu_courserplanlist=self.get_stu_courseplanlist(stu_No,stu_plan_name,stu_plan_id)
            stu_eleactive_info=self.get_stu_eleactive(semeId,stu_No)
            stu_cur_eleactive=stu_eleactive_info[0]
            stu_eleactive=stu_eleactive_info[1]
            tobeelectlist = copy.deepcopy(stu_courserplanlist)
            if len(stu_courserplanlist)>0 and len(stu_eleactive)>0:
                for course in stu_courserplanlist:
                    print(course)
                print("remove 前---------------")
                for havecourse in stu_eleactive:
                    print(havecourse)
                print("havecourse ---------------")

                for course in stu_courserplanlist:
                    for havecourse in stu_eleactive:
                        if course['courseId']==havecourse['courseId']:
                            print('remove:' + str(course))
                            if course in tobeelectlist:
                                tobeelectlist.remove(course)
                print("remove 后---------------")
                self.selectCourseService.delete_selctcourse(stu_No)
                for course in tobeelectlist:
                    self.selectCourseService.insert_selctcourse(stu_No, course)
        return stu_cur_eleactive,tobeelectlist

    # 获取学生选课计划
    def get_stu_courseplanlist(self,login_name,stu_plan_name,stu_plan_id):
        dateutil = DateUtil.DateUtil()
        semenum=dateutil.getSCTermNo(stu_plan_name)
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/courseplan/list_stu'
        post_data = {
            'page': 1,
            'pageSize':100,
            'coursePlan.planId':stu_plan_id,
            'coursePlan.semenum':semenum
        }
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                print('选课信息---' + response.text)
                stu_course_json = json.loads(response.text)
                stu_course_plan=stu_course_json['pager']['datas']
        except:
            self.log(neterror_msg, True)
        return stu_course_plan


    # 获取学生本学期已选课程
    def get_stu_eleactive(self,semeId,studentNo):
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/eleactive/list'
        post_data = {
            'page': 1,
            'pageSize': 100,
            'eleactive.studentNo': studentNo
        }
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                stu_course_json = json.loads(response.text)
                stu_elective = stu_course_json['pager']['datas']
                stu_have_elect=[] # 历史已选课程
                stu_cur_elect=[]  # 当前已经课程
                for course in stu_elective:
                    iscourseinhis=self.check_ifcourseinhis(semeId,studentNo,course['courseId'])
                    if "examScore" in course or iscourseinhis:
                        stu_have_elect.append(course)
                    else:
                        stu_cur_elect.append(course)
        except:
            self.log(neterror_msg, True)
        return stu_cur_elect,stu_have_elect

    def check_ifcourseinhis(self,semeId,studentNo,courseId):
        stu_his_elective=self.get_stu_his_eleactive(semeId,studentNo)
        for course in stu_his_elective:
            if course['courseId']==courseId:
                return True
        return False

    def get_stu_his_eleactive(self,semeId,studentNo):
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/eleactive/list2'
        post_data = {
            'page': 1,
            'pageSize': 100,
            'eleactive.semeId':semeId,
            'eleactive.studentNo': studentNo
        }
        try:
            response = self.session.post(request_url, data=post_data, headers=self.headers)
            if response.status_code == 200:
                stu_course_json = json.loads(response.text)
                stu_his_elective = stu_course_json['pager']['datas']
        except:
            self.log(neterror_msg, True)
        return stu_his_elective


    # 显示单个学生的作业进度
    def show_dowork_proc(self,maximum,value):
        if self.utiltools is not None:
            self.utiltools.show_procbar_proc(maximum,value)

    # 记日志
    def log(self,logstr,islog=False):
        if self.utiltools is not None:
            self.utiltools.log(logstr,islog)
        else:
            print(logstr)

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

    def getifforceselectcourse(self):
        forceselectcourse = self.config.get_configvalue('setting', 'forceselectcourse')
        if forceselectcourse is not None and forceselectcourse=='True':
            forceselectcourse = True
        else:
            forceselectcourse = False
        return forceselectcourse


    # 设置状态栏的状态信息
    def set_status(self,str):
        if self.utiltools is not None:
            self.utiltools.set_status_bar(str)

    def check_selectwork_ishaveinitdata(self):
        return self.selectworkService.ishaveinitdata()

    def check_selectcourse_ishaveinitdata(self):
        return self.selectCourseService.ishaveinitdata()

    def init_selectworkdata(self,filepath=None):
        self.selectworkService.initdata(filepath)

    def init_selectcoursedata(self,filepath=None):
        self.selectCourseService.initdata(filepath)


if __name__=='__main__':
    service=Service()
    #service.login(login_name='201820113109',login_psw='806854137')
    #service.geteleactive(semeId='40',studentNo='202020121200')
    #service.getstudentpaper(1002,1107)
    #service.getstudentpaper('201820113109','684','医古文B',684)
    #print(service.getstudentlearninfo('46903'))
    #service.student_selectcourse('201820112006','466183314')
    stud_info=service.login(login_name='201820112006', login_psw='466183314')
    service.stu_selectcourse(stud_info,16)
