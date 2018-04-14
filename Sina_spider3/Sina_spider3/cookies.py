# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

import random
import logging

cookiefilename = '/usr/apps/sinaspider/mycookies.txt'#@TODO change this

logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING


myWeiBo = [
    ('15945757604','hn120211'),
    ('18783124694','hn120211'),
    ('18745320194','hn120211'),
    ('15945757304','hn120211'),
    ('15946372542','hn120211'),
    ('18714442954','hn120211'),
    ('15945759954','hn12021'),
]

def builddict(string):
    cookiedic ={}
    dictstr='{'
    linelist = string.split(';')
    for line in linelist:
        key = line.split('=')[0]
        value = line.split('=')[1]
        dictstr = dictstr+'"'+key+'"'+':'+"'"+value+"'"+','
        cookiedic[key]=value
    dictstr= dictstr.rstrip(',')
    dictstr= dictstr+'}'
    #print(dictstr)
    return cookiedic

def getcookiefromfile():
    newcookielist =[]
    with open(cookiefilename,'r+') as f:
        cookielist = f.readlines()
        for cookies in cookielist:
            cookies = cookies.rstrip('\n')
            cookieaccount = cookies.split(',')[0].lstrip('(')
            cookiepwd = cookies.split(',')[1]
            cookiecontent = cookies.split(',')[2].rstrip(')')
            cookiedict =builddict(cookiecontent)
            #print(str(cookiedict))
            #cookiedict = json.loads(cookiedict)
            newcookielist.append((cookieaccount,cookiepwd,cookiedict))#(str,str,dict)
    return newcookielist
    #return mycookies

       
def getCookie(account, password):
    cookielist = getcookiefromfile()
    cookie = cookielist[random.randint(0,len(cookielist)-1)]
    return cookie
    #return get_cookie_from_login_sina_com_cn(account, password)

def initCookie( spiderName):
    """ 获取所有账号的Cookies (账号,密码,cookie内容) """
    
    cookieaccountlist=[]
    cookielist = getcookiefromfile()
    for cookies in cookielist:
        cookieaccountlist.append(cookies[0])
        
    print(cookieaccountlist)
    
    for weibo in myWeiBo:
        if weibo[0] not in cookieaccountlist:
            #print(weibo[0]+'not in the file,try to get one')
            cookie = getCookie(weibo[0],weibo[1])
            #print(type(cookie))
            #print('getcookie'+str(cookie))
            cookierecord = (weibo[0],weibo[1],cookie)
            cookielist.append(cookierecord)
        
    #writecookietofile(cookielist)