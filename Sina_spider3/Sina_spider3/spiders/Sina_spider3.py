# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

import scrapy
import logging
import datetime
import requests
import re
from lxml import etree
from Sina_spider3.weiboID import weiboID
from scrapy.selector import Selector
from scrapy.http import Request
from Sina_spider3.items import TweetsItem, InformationItem, RelationshipsItem,Topic_TweeetItem



class Spider(scrapy.Spider):
    name = "Sina_spider3"
    host = "https://weibo.cn"
    start_urls = list(set(weiboID))
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    AS_FANS = 500
    """
    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)

    """
    def start_requests(self):
        keyword = "%E5%A4%B4%E5%8F%B7%E7%8E%A9%E5%AE%B6"
        for page in range(1,100):
            yield Request(url="https://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&advancedfilter=1&hasori=1&sort=time&page=" +str(page), callback=self.parse_topicSearch)

    def parse_topicSearch(self,response):
        topic_tweetItem = Topic_TweeetItem()
        selector= Selector(response)
        divs =  selector.xpath('body/div[@class="c" and @id]')
        for div in divs:
            nicknames = div.xpath('div/a[@class="nk"]/text()')
            userlinks = div.xpath('div/a[@class="nk"]/@href')
            tweet_contents = ''.join(div.xpath('div/span[@class="ctt"]//text()').extract())
            sources=div.xpath('div/span[@class="ct"]/text()')
            tweet_reacts = ';'.join(div.xpath('//a/text()').extract())
            likes = re.findall('赞\[(\d+)\]',tweet_reacts)
            retweets = re.findall('转发\[(\d+)\]',tweet_reacts)
            comments = re.findall('评论\[(\d+)\]',tweet_reacts)
            
            if nicknames and nicknames[0]:
                topic_tweetItem['Nickname']=nicknames[0].extract().replace(u"\xa0", "")
            else:
                topic_tweetItem['Nickname']='not specified'
                
            if userlinks and userlinks[0]:
                topic_tweetItem['UserLink']=userlinks[0].extract()
            else:
                topic_tweetItem['UserLink']='not spercified'
                
            if tweet_contents and tweet_contents:
                topic_tweetItem['Content']=tweet_contents.replace(u"\xa0", "").replace(u'\u200b','').replace(u'\U0001f3ae','')
                print('topic:'+tweet_contents.replace(u"\xa0", ""))
            else:
                topic_tweetItem['Content']='not specified'
                
            if likes and likes[0]:
                topic_tweetItem['LikeNum']=likes[0]
            else:
                topic_tweetItem['LikeNum']='not specified'
                
            if retweets and retweets[0]:
                topic_tweetItem['RetweetNum']=retweets[0]
            else:
                topic_tweetItem['RetweetNum']='not specified'
                
            if comments and comments[0]:
                topic_tweetItem['CommentNum']=comments[0]
            else:
                topic_tweetItem['CommentNum']='not specified'
                
            if sources and sources[0]:
                topic_tweetItem['Source']=sources[0].extract().replace(u"\xa0", "")
            else:
                topic_tweetItem['Source']='not specified'
            yield topic_tweetItem
    def parse_information(self, response):
        """ 抓取个人信息 """
        informationItem = InformationItem()
        selector = Selector(response)
        #print('response body is :'+response.body.decode('utf8'))
        print('response url is :'+response.url)
        ID = re.findall('(\d+)/info', response.url)[0]
        try:
            text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
            nickname = re.findall('昵称[：:]?(.*?);', text1)
            gender = re.findall('性别[：:]?(.*?);', text1)
            place = re.findall('地区[：:]?(.*?);', text1)
            briefIntroduction = re.findall('简介[：:]?(.*?);', text1)
            birthday = re.findall('生日[：:]?(.*?);', text1)
            sexOrientation = re.findall('性取向[：:]?(.*?);', text1)
            sentiment = re.findall('感情状况[：:]?(.*?);', text1)
            vipLevel = re.findall('会员等级[：:]?(.*?);', text1)
            authentication = re.findall('认证[：:]?(.*?);', text1)
            url = re.findall('互联网[：:]?(.*?);', text1)

            informationItem["_id"] = ID
            if nickname and nickname[0]:
                informationItem["NickName"] = nickname[0].replace(u"\xa0", "")
            else:
                informationItem["NickName"]='not specified'
                
            if gender and gender[0]:
                informationItem["Gender"] = gender[0].replace(u"\xa0", "")
            else:
                informationItem["Gender"]='not specified'
                
            if place and place[0]:
                place = place[0].replace(u"\xa0", "").split(" ")
                informationItem["Province"] = place[0]
                if len(place) > 1:
                    informationItem["City"] = place[1]
                else:
                    informationItem["City"] ='not specified'
            else:
                informationItem["Province"]='not specified'
                informationItem["City"] = 'not specified'
                
            if briefIntroduction and briefIntroduction[0]:
                informationItem["BriefIntroduction"] = briefIntroduction[0].replace(u"\xa0", "")
            else:
                 informationItem["BriefIntroduction"] ='not specified'
                 
            if birthday and birthday[0]:
                try:
                    birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                    informationItem["Birthday"] = birthday - datetime.timedelta(hours=8)
                except Exception:
                    informationItem['Birthday'] = birthday[0]   # 有可能是星座，而非时间
            else:
                informationItem['Birthday'] ='not specified'
                
            if sexOrientation and sexOrientation[0]:
                if sexOrientation[0].replace(u"\xa0", "") == gender[0]:
                    informationItem["SexOrientation"] = "同性恋"
                else:
                    informationItem["SexOrientation"] = "异性恋"
            else:
                informationItem["SexOrientation"] = 'not specified'
                
            if sentiment and sentiment[0]:
                informationItem["Sentiment"] = sentiment[0].replace(u"\xa0", "")
            else:
                informationItem["Sentiment"] ='not specified'
                
            if vipLevel and vipLevel[0]:
                informationItem["VIPlevel"] = vipLevel[0].replace(u"\xa0", "")
            else:
                informationItem["VIPlevel"] ='not specified'
                
            if authentication and authentication[0]:
                informationItem["Authentication"] = authentication[0].replace(u"\xa0", "")
            else:
                informationItem["Authentication"] ='not specified'
                
            if url:
                informationItem["URL"] = url[0]
            else:
                informationItem["URL"] = 'not specified'
                
            try:
                urlothers = "https://weibo.cn/attgroup/opening?uid=%s" % ID
                r = requests.get(urlothers, cookies=response.request.cookies, timeout=5)
                if r.status_code == 200:
                    selector = etree.HTML(r.content)
                    texts = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
                    if texts:
                        num_tweets = re.findall('微博\[(\d+)\]', texts)
                        num_follows = re.findall('关注\[(\d+)\]', texts)
                        num_fans = re.findall('粉丝\[(\d+)\]', texts)
                        if num_tweets:
                            informationItem["Num_Tweets"] = int(num_tweets[0])
                        else:
                            informationItem["Num_Tweets"] = 'not specified'
                            
                        if num_follows:
                            informationItem["Num_Follows"] = int(num_follows[0])
                        else:
                            informationItem["Num_Follows"] = 'not specified'
                            
                        if num_fans:
                            informationItem["Num_Fans"] = int(num_fans[0])
                        else:
                            informationItem["Num_Fans"] = 'not specified'
            except :
                pass
        except :
            pass
        else:
            yield informationItem
        #yield Request(url="https://weibo.cn/%s/profile?filter=1&page=1" % ID, callback=self.parse_tweets, dont_filter=True)
        yield Request(url="https://weibo.cn/%s/follow" % ID, callback=self.parse_relationship, dont_filter=True)
        #yield Request(url="https://weibo.cn/%s/fans" % ID, callback=self.parse_relationship, dont_filter=True)

    def parse_tweets(self, response):
        """ 抓取本用户发过的微博 """
        selector = Selector(response)
        ID = re.findall('(\d+)/profile', response.url)[0]
        divs = selector.xpath('body/div[@class="c" and @id]')
        for div in divs:
            try:
                tweetsItems = TweetsItem()
                id = div.xpath('@id').extract_first()  # 微博ID
                content = div.xpath('div/span[@class="ctt"]//text()').extract()  # 微博内容
                cooridinates = div.xpath('div/a/@href').extract()  # 定位坐标
                like = re.findall('赞\[(\d+)\]', div.extract())  # 点赞数
                transfer = re.findall('转发\[(\d+)\]', div.extract())  # 转载数
                comment = re.findall('评论\[(\d+)\]', div.extract())  # 评论数
                others = div.xpath('div/span[@class="ct"]/text()').extract()  # 求时间和使用工具（手机或平台）

                tweetsItems["_id"] = ID + "-" + id
                tweetsItems["ID"] = ID
                if content:
                    tweetsItems["Content"] = " ".join(content).strip('[位置]')  # 去掉最后的"[位置]"
                else:
                    tweetsItems["Content"] = 'not specified'
                    
                if cooridinates:
                    cooridinates = re.findall('center=([\d.,]+)', cooridinates[0])
                    if cooridinates:
                        tweetsItems["Co_oridinates"] = cooridinates[0]
                else:
                    tweetsItems["Co_oridinates"] = 'not specified'
                    
                if like:
                    tweetsItems["Like"] = int(like[0])
                else:
                     tweetsItems["Like"] = 'not specified'
                     
                if transfer:
                    tweetsItems["Transfer"] = int(transfer[0])
                else:
                    tweetsItems["Transfer"] = 'not specified'
                    
                if comment:
                    tweetsItems["Comment"] = int(comment[0])
                else:
                    tweetsItems["Comment"] = 'not specified'
                    
                if others:
                    others = others[0].split('来自')
                    tweetsItems["PubTime"] = others[0].replace(u"\xa0", "")
                    if len(others) == 2:
                        tweetsItems["Tools"] = others[1].replace(u"\xa0", "")
                else:
                    tweetsItems["PubTime"] = 'not specified'
                    tweetsItems["Tools"] ='not specified'
                yield tweetsItems
            except :
                pass

        url_next = selector.xpath('body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="下页"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], callback=self.parse_tweets, dont_filter=True)

    def parse_relationship(self, response):
        """ 爬取个人关系里面的关注用户，找到本用户所关注并且粉丝数大于一定数量的用户，迭代爬取 """
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她"]/@href').extract()
        fanscountlist = selector.xpath('//table//td[@valign="top"][2]//text()')
        fansindex = 0
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        for uid in uids:
            fanscounttext = fanscountlist[1+3*fansindex]
            fans = re.findall('粉丝(\d+)人',str(fanscounttext),re.S)[0]
            fans = int(fans)
            fansindex=fansindex+1
            if fans>self.AS_FANS:
                relationshipsItem = RelationshipsItem()
                relationshipsItem["followID"] = uid
                yield relationshipsItem
                yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)
                
        next_url = selector.xpath('//a[text()="下页"]/@href').extract()
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse_relationship, dont_filter=True)
            