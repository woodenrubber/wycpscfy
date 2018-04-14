# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

import os
import random
import logging
from Sina_spider3 import myagents
from Sina_spider3 import cookies #import initCookie, updateCookie, removeCookie
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import requests
import json

logger = logging.getLogger(__name__)
proxyfilepath ='/usr/apps/sinaspider/myproxy.txt'
class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(myagents.agents)
        request.headers["User-Agent"] = agent

class ProxyMiddleware(object):
    #构建代理IP
    def getProxy():
        global proxyfilepath
        proxylist = []
        proxyres = requests.get('http://proxy.nghuyong.top').text
        totalproxies = json.loads(proxyres)['num']
        if (totalproxies>0):
            proxylist=json.loads(proxyres)['data']
            with open(proxyfilepath,'w') as f:
                for proxy in proxylist:
                    f.write(proxy['ip_and_port']+'\n')
                    proxylist.append(proxy['ip_and_port'])
            #return proxylist#return a list
        return proxylist
        

    def process_request(self,request,spider):
        global proxyfilepath
        proxylist =[]
        '''
        with open(proxyfilepath,'r') as f:
            proxyread= f.readlines()
            for proxies in proxyread:
                proxies = proxies.strip('\n')
                proxylist.append(proxies)
                
        if len(proxylist)==0:
            proxylist = self.getProxy()
        if len(proxylist)!=0:
            proxy = proxylist[random.randint(0,len(proxylist)-1)]
            print('using proxy:'+proxy)
            request.meta['proxy'] = "http://"+proxy
        
        '''
class CookiesMiddleware(RetryMiddleware):
    """ 维护Cookie """

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        cookies.initCookie(crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        cookielist = cookies.getcookiefromfile()
        cookietemp = cookielist[random.randint(0,len(cookielist)-1)]
        cookieaccount = cookietemp[0]
        cookiepwd = cookietemp[1]
        cookiecontent = cookietemp[2]
        #print('using cookie:')
        #print(cookiecontent)
        request.cookies = cookiecontent#json.loads(cookiecontent)
        request.meta["accountText"]=cookieaccount+"--"+cookiepwd

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                redirect_url = str(redirect_url)
                print(redirect_url)
                if "passport.weibo" in redirect_url or "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    logger.warning("One Cookie need to be updating...")
                    #cookies.updateCookie(request.meta['accountText'], spider.name)
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    logger.warning("One Account is locked! Remove it!")
                    #cookies.removeCookie(request.meta["accountText"], spider.name)
                elif "weibo.cn/pub" in redirect_url:
                    logger.warning(
                        "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except :
                raise IgnoreRequest
        elif response.status in [403, 414]:
            logger.error("%s! Stopping..." % response.status)
            os.system("pause")
        else:
            return response
