# encoding=utf-8
# ------------------------------------------
#   版本：4.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

import random
import logging
from Spyder import myagents
from Spyder import cookies 
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import requests
import json

logger = logging.getLogger(__name__)
proxyfilepath ='F:\desktop\Spyder\myproxy.txt'
class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(myagents.agents)
        request.headers["User-Agent"] = agent

class ProxyMiddleware(object):
    '''
    #构建代理IP
    def getProxy(self):
        global proxyfilepath
        proxylist = []
        proxyres = requests.get('http://proxy.nghuyong.top').text
        totalproxies = json.loads(proxyres)['num']
        if (totalproxies>0):
            proxylists=json.loads(proxyres)['data']
            with open(proxyfilepath,'w') as f:
                for proxy in proxylists:
                    f.write(proxy['ip_and_port']+'\n')
                    proxylist.append(proxy['ip_and_port'])
            #return proxylist#return a list
        return proxylist
        

    def process_request(self,request,spider):
        global proxyfilepath
        proxylist =[]
        with open(proxyfilepath,'r') as f:
            proxyread= f.readlines()
            for proxies in proxyread:
                proxies = proxies.strip('\n')
                proxylist.append(proxies)
                
        if len(proxylist)==0:
            proxylist = self.getProxy()
        else:
            proxy = proxylist[random.randint(0,len(proxylist)-1)]
            print('using proxy:'+proxy)
            request.meta['proxy'] = "http://"+proxy
    ''' 
    pass 

     
class CookiesMiddleware(RetryMiddleware):
    """ 维护Cookie 以及处理相关响应"""

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
        cookies.initCookie(crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        if 'weibo.cn' in request.url:
            self.process_weibo_request(request,spider)
        elif 'movie.douban.com' in request.url:
            self.process_douban_request(request,spider)
        
            
    """ 为豆瓣爬虫加上cookie，模拟登录 """
    def process_douban_request(self, request, spider):
        mycookie = 'bid=baf3NkFR5Dw; ll="118318"; __yadk_uid=zInDRd9Ba91W4YuGziZo9EZeYGVhd7JM; _vwo_uuid_v2=DEC30022151DB337E1E8FF98E02FED6FC|9a2c17301585d5e122f36ea34f221915; ps=y; push_noty_num=0; push_doumail_num=0; ap=1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1523971835%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DwjWb-byldIhtmvrCkBfjnJMdtsb6je6rNmYFXQeHdkcBeMXOmi-LG4ymlrjNoXv3%26wd%3D%26eqid%3Df96e2ae100001791000000035ad5f6f8%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1002271375.1523806427.1523965111.1523971836.3; __utmb=30149280.0.10.1523971836; __utmc=30149280; __utmz=30149280.1523971836.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.654526791.1523806433.1523965112.1523971836.3; __utmb=223695111.0.10.1523971836; __utmc=223695111; __utmz=223695111.1523971836.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="177486474:XeNECqqpT9U"; ck=abc5; _pk_id.100001.4cf6=653de6e9975c7c6e.1523806452.4.1523972031.1523965320.'
        request.cookies=self.builddict(mycookie)
        return request
        
    ''' 因为request接受的cookie是字典形式，所以要把从浏览器赋值过来的cookie解析成字典形式 '''
    def builddict(self,string):
        dictstr='{'
        linelist = string.split(';')
        for line in linelist:
            key = line.split('=')[0]
            value = line.split('=')[1]
            value=value.lstrip('"').rstrip('"')
            dictstr = dictstr+'"'+key+'"'+':'+'"'+value+'"'+','
        dictstr= dictstr.rstrip(',')
        dictstr= dictstr+'}'
        #print(dictstr)
        return json.loads(dictstr)
    
    ''' 处理微博的请求，为请求添加cookie '''
    def process_weibo_request(self, request, spider):
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
        if 'weibo.cn' in response.url:
            return self.process_weibo_response(request,response,spider)
        elif 'movie.douban.com' in response.url:
            return self.process_douban_response(request,response,spider)
        else:
            return response
    ''' 处理微博的响应 '''
    def process_weibo_response(self, request, response, spider):
        
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                redirect_url = str(redirect_url)
                print(redirect_url)
                if "passport.weibo" in redirect_url or "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    logger.warning("One Cookie need to be updated...")
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    logger.warning("One Account is locked! Remove it!")
                elif "weibo.cn/pub" in redirect_url:
                    logger.warning(
                        "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except :
                raise IgnoreRequest
        elif response.status in [403, 414]:
            logger.error("%s! http host return 403..." % response.status)
            reason = response_status_message(response.status)
            print('change ip proxy and retrying...')
            proxyres = requests.get('http://proxy.nghuyong.top').text
            totalproxies = json.loads(proxyres)['num']
            if (totalproxies>0):
                proxylist=json.loads(proxyres)['data']
                proxy = random.choice(proxylist)
                request.meta['proxy'] ="http://"+proxy['ip_and_port']
                return self._retry(request,reason,spider)
        else:
            return response

    ''' 处理豆瓣的响应 '''
    def process_douban_response(self, request, response, spider):
        if response.status in [403, 414,302]:
            reason = response_status_message(response.status)
            print('change ip proxy and retrying...')
            proxyres = requests.get('http://proxy.nghuyong.top').text
            totalproxies = json.loads(proxyres)['num']
            if (totalproxies>0):
                proxylist=json.loads(proxyres)['data']
                proxy = random.choice(proxylist)
                request.meta['proxy'] ="http://"+proxy['ip_and_port']
                return self._retry(request,reason,spider)
        else:
            return response