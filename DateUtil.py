# -*- coding: utf-8 -*-
"""
    :author: XieJava
    :url: http://ishareread.com
    :copyright: © 2019 XieJava <xiejava@ishareread.com>
    :license: MIT, see LICENSE for more details.
"""
import datetime
import time
import calendar as c
class DateUtil:

    def days(self,str1,str2):
        date1=datetime.datetime.strptime(str1[0:10],"%Y-%m-%d")
        date2=datetime.datetime.strptime(str2[0:10],"%Y-%m-%d")
        num=(date1-date2).days
        return num

    def months(self,str1,str2):
        year1=datetime.datetime.strptime(str1[0:10],"%Y-%m-%d").year
        year2=datetime.datetime.strptime(str2[0:10],"%Y-%m-%d").year
        month1=datetime.datetime.strptime(str1[0:10],"%Y-%m-%d").month
        month2=datetime.datetime.strptime(str2[0:10],"%Y-%m-%d").month
        num=(year1-year2)*12+(month1-month2)
        return num

    def getTermDate(self,term):
        termyear = term[0:4]
        if term.find('春')>0:
            termdate=termyear+'-03-01'
        elif term.find('秋')>0:
            termdate = termyear + '-09-01'
        termdate=str(datetime.datetime.strptime(termdate, '%Y-%m-%d'))
        print(termdate)
        return termdate

    def getTermNo(self,term,curdate):
        termcycle=6    #半年一个周期
        termDate=self.getTermDate(term)
        monthInterval=self.months(curdate,termDate)
        termNo=monthInterval//termcycle+1
        return termNo

    def getSCTermNo(self,term):
        curdate = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        termNo = self.getTermNo(term, curdate)
        scTermNo=termNo+1 #本学期选下学期的课程
        return scTermNo

if __name__ == '__main__':
    dateutil=DateUtil()
    #month_str=dateutil.months('2021-02-01 08:18:09','2020-11-01 10:19:33')
    #print(month_str)
    curdate=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(curdate)
    termNo=dateutil.getSCTermNo('2020秋')
    print(termNo)
