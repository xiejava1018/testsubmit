# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import requests
import json

class Login(object):
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

    def login(self,login_name,login_psw):
        post_data={
            'student.studentNo':login_name,
            'student.pwd':login_psw
        }

        response=self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code==200:
            print(response)

        response=self.session.get(self.logined_url,headers=self.headers)
        if response.status_code==200:
            print(response)

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
            print(response.text)
            eleactivedata=json.loads(response.text)
            if eleactivedata is not None:
                courselist=eleactivedata['pager']['datas']
                for course in courselist:
                    semeId=course['semeId']
                    courseId = course['courseId']
                    login.getstudentcursework(semeId=semeId,courseId=courseId)


    def getstudentcursework(self,semeId,courseId):
        #作业列表URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_list'
        post_data={
            'semeId':semeId,
            'courseId':courseId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            paperdata=json.loads(response.text)
            if paperdata is not None:
                for paper in paperdata:
                    login.getstudentpaper(paper['paperId'])


    def getstudentpaper(self,paperId):
        #试卷URL
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/paper'
        paperId=998
        post_data={
            'paperId':paperId
        }
        response = self.session.post(request_url, data=post_data,headers=self.headers)
        if response.status_code == 200:
            paperinfo=json.loads(response.text)
            print(len(paperinfo))
            for queitem in paperinfo:
                queitem['quelib']['okFlag']=queitem['quelib']['ok1']
                #print(json.dumps(queitem,ensure_ascii=False))
            subpaper=json.dumps(paperinfo,ensure_ascii=False)
            login.submitpaper(subpaper)

    def getstudentworktest(self,paperId):
        # 试卷URL
        request_url = 'https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/work_test'
        post_data = {
            'paperId': paperId
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('test---'+response.text)


    def submitpaper(self,subpaper):
        request_url='https://jxjyxb.bucm.edu.cn/api/v1/student/coursework/submit_work?paperId=998&workId=1103'
        post_data={
            'sub':subpaper
        }
        response = self.session.post(request_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print('submit paper---'+response.text)
if __name__=='__main__':
    login=Login()
    login.login(login_name='202020121200',login_psw='1qaz2wsx')
    login.geteleactive(semeId='40',studentNo='202020121200')