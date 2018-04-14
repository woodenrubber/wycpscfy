# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 23:45:36 2018

@author: Li-We
"""
import base64
import requests
import time
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import re
import rsa
import binascii
from lxml import etree
'''
================================================================datas 
'''

myWeiBo = [
    ('15945757604', 'hn120211'),
    ('18783124694','hn120211'),
    ('18745320194','hn120211'),
    ('15945757304','hn120211'),
    ('15946372542','hn120211'),
    ('18714442954','hn120211'),
    ('15945759954','hn12021'),
]
cookiefilename = 'F:/Desktop/mycookies1.txt'
cookielistsInit =[('a','p','cookie'),('b','p2','cookie2'),('v','gh','cookie3')]
jsondic = {
        'name':'aname',
        'password':'passrrr',
        'cookie':'23kjje4o'}

sourcehtml='<table><tr><td valign="top" style="width: 52px"><a href="https://weibo.cn/u/1971874241"><img src="http://tvax3.sinaimg.cn/crop.0.0.1008.1008.50/758869c1ly8fpapphz4ppj20s00s03zv.jpg" alt="pic" /></a></td><td valign="top"><a href="https://weibo.cn/u/1971874241">姜海荣_Harrison</a><img src="https://h5.sinaimg.cn/upload/2016/05/26/319/5338.gif" alt="V"/><br/>粉丝7086人<br/><a href="https://weibo.cn/attention/add?uid=1971874241&amp;rl=1&amp;st=481697">关注他</a></td></tr></table><div class="s"></div>'
proxyfilepath ='F:/Desktop/Data/myproxy.txt'
sourcehtml2='<div class="c" id="M_Gb6mckUo8"><div><a class="nk" href="https://weibo.cn/yuanaixing">老K龙飞</a><img src="https://h5.sinaimg.cn/upload/2016/05/26/319/5338.gif" alt="V"/><img src="https://h5.sinaimg.cn/upload/2016/05/26/319/donate_btn_s.png" alt="M"/><span class="ctt">:<a href="http://weibo.cn/pages/100808topic?extparam=%E5%A4%B4%E5%8F%B7%E7%8E%A9%E5%AE%B6&amp;from=feed">#头号玩家#</a> 我的评分：★★★ 在这个所谓泛娱乐、信息接收碎片化的年代里，我们极容易被其深深吸引，被既定好的世界观、规则所引人入胜，对某项东西的沉迷虽然有如昙花一现，但新鲜事物接踵而来，娱乐和物质上瘾几乎成为人人常态。面对这个越... <a href="https://weibo.cn/sinaurl?f=w&amp;u=http%3A%2F%2Ft.cn%2FROgZcqD&amp;ep=Gb6mckUo8%2C3553539622%2CGb6mckUo8%2C3553539622">http://t.cn/ROgZcqD</a>… ​</span></div><div><a href="https://weibo.cn/mblog/pic/Gb6mckUo8?rl=1"><img src="http://wx4.sinaimg.cn/wap180/d3ceb626gy1fq4zdz1t80j20qo1bhgum.jpg" alt="图片" class="ib" /></a>&nbsp;<a href="https://weibo.cn/mblog/oripic?id=Gb6mckUo8&amp;u=d3ceb626gy1fq4zdz1t80j20qo1bhgum">原图</a>&nbsp;<a href="https://weibo.cn/attitude/Gb6mckUo8/add?uid=6515389081&amp;rl=1&amp;st=c06da0">赞[0]</a>&nbsp;<a href="https://weibo.cn/repost/Gb6mckUo8?uid=3553539622&amp;rl=1">转发[0]</a>&nbsp;<a href="https://weibo.cn/comment/Gb6mckUo8?uid=3553539622&amp;rl=1#cmtfrm" class="cc">评论[0]</a>&nbsp;<a href="https://weibo.cn/fav/addFav/Gb6mckUo8?rl=1&amp;st=c06da0">收藏</a><!---->&nbsp;<span class="ct">2分钟前&nbsp;来自性别为K的iPhone 7 Plus</span></div></div><div class="s">'
'''
================================================================methods 
'''

def get_cookie_from_login_sina_com_cn(username,password):
    '''登陆新浪微博，获取登陆后的Cookie，返回到变量cookies中'''
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.18)%'+username
    html = requests.get(url).content
    html = str(html)
    servertime = re.findall('"servertime":(.*?),',html,re.S)[0]
    nonce = re.findall('"nonce":"(.*?)"',html,re.S)[0]
    pubkey = re.findall('"pubkey":"(.*?)"',html,re.S)[0]
    rsakv = re.findall('"rsakv":"(.*?)"',html,re.S)[0]

    username = base64.b64encode(username.encode('utf8')) #加密用户名
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
    passwd = rsa.encrypt(message.encode('utf8'), key) #加密
    passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。

    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    data = {'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': passwd,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv' : rsakv,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    html = requests.post(login_url,data=data).content
    html = str(html)
    print(html)
    urlnew = re.findall("location.replace\(\"(.*?)\"",html,re.S)[0]
    #发送get请求并保存cookies
    cookies = requests.get(urlnew).cookies
    cookies = requests.utils.dict_from_cookiejar(cookies)
    print(type(cookies))
    print('original get cookies:'+str(cookies))
    return cookies


def getcookiefromfile():
    newcookielist =[]
    with open(cookiefilename,'r+') as f:
        cookielist = f.readlines()
        print(str(len(cookielist)))
        print(cookielist)
        for cookies in cookielist:
            cookies = str(cookies)
            print(type(cookies))
            print(cookies)
            cookies = cookies.rstrip('\n')
            cookieaccount = cookies.split(',')[0].lstrip("('").rstrip("'")
            cookiepwd = cookies.split(',')[1].lstrip(" '").rstrip("'")
            cookiecontent = cookies.split(',')[2].lstrip(" '").rstrip("')")
            newcookielist.append((cookieaccount,cookiepwd,cookiecontent))
            
    return newcookielist
def writecookietofile(cookielist):
    with open(cookiefilename,'w') as f:
        for cookies in cookielist:
            f.writelines(str(cookies)+'\n')
    
def getProxy():
    global proxyfilepath
    proxyres = requests.get('http://proxy.nghuyong.top').text
    totalproxies = json.loads(proxyres)['num']
    if (totalproxies>0):
        proxylist=json.loads(proxyres)['data']
        with open(proxyfilepath,'w') as f:
            for proxy in proxylist:
                f.write(proxy['ip_and_port']+'\n')
        #return proxylist#return a list
    
def readproxy():
    proxylist =[]
    with open(proxyfilepath,'r') as f:
        proxyread= f.readlines()
        for proxies in proxyread:
            proxies = proxies.strip('\n')
            proxylist.append(proxies)
            
    print(proxylist)
'''
================================================================uses
'''
'''
writecookietofile(cookielistsInit)
mycookielist = getcookiefromfile()
print(len(mycookielist))
for cookies in mycookielist:
	print(cookies[0])
'''
'''
with open('jsontest.json','w') as f:
    string = json.dumps(jsondic)
    string.replace("'",'"')
    print('string is:'+string)
    jsondic = json.loads(string)
    string =json.dump(jsondic,f)
    #string.replace("'",'"')
with open('jsontest.json','r')as f:
    res = f.read()
    res = res.replace("'",'"')
    jsondicload = json.loads(res)
    print(type(jsondicload))
    print(jsondicload)
'''
#get_cookie_from_login_sina_com_cn('15945759954','hn12021')
#string ="{"_T_WM":'9691488ba2c4d38dad8a21e056d6880c'," SUB":'_2A253w1UADeRhGeBL6lcQ8yzOzzqIHXVVTHtIrDV6PUJbkdAKLVbwkW1NR1HEz4LJrcC8AtlyiFjTKlM9UgzkS_uW'," SUHB":'0z1Aid2IDKz4jS',"SCF":'Ao8DS1hkcmUQulFOaybEezLjtT2DYkStwnEfwCbyXhcl4cyDT32aqTIFVVmZE_Tv4R-GGjTejAmXrOQaJ4IXLD8.'," SSOLoginState":'1523000656'}'
selector = etree.HTML(sourcehtml2)
'''
fanscount =selector.xpath('//table//td')
print(fanscount)
for fans in fanscount:
    linkselector = etree.HTML(fans)
    links = linkselector.xpath('/a/@href')
    print(links)
'''
#getProxy()
#readproxy()
#fanscount = re.findall('粉丝(\d+)人',fanscount)[0]
#print(type(int(fanscount)))
#print(fanscount)
#tweet_attr = ';'.join(selector.xpath('body/div[@class="c"]/div[2]//text()'))
#tweet_list = selector.xpath('body/div[@class="c"]/div[2]//text()')
#likes = ';'.join(tweet_list)
#likenum = re.findall('评论\[(\d+)\]',likes)[0]
#print(likes)
#sources=selector.xpath('body/div[@class="c"]//span[@class="ct"]/text()')
#print(sources)
divs =  selector.xpath('body/div[@class="c" and @id]')
for div in divs:
    nicknames = div.xpath('div//text()')
    tweet_reacts = ';'.join(div.xpath('//a/text()'))
    print(str(nicknames[2]))