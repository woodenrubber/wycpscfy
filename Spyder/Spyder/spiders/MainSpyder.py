# encoding=utf-8
# ------------------------------------------
#   版本：4.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

import scrapy
import re
import time
from scrapy.selector import Selector
from scrapy.http import Request
from Spyder.items import Topic_TweeetItem,DBScrapyItem,MtimescrapyItem
from Spyder.spiders.wzApi import wzAPI


class Spider(scrapy.Spider):
    name = "mainspyder"

    ''' scrapy默认请求队列 '''
    def start_requests(self):
        
       
        ''' 豆瓣爬虫初始URL '''
        douban_start_url='https://movie.douban.com/subject/4920389/comments?start=20&limit=20&sort=new_score&status=P&percent_type='
        yield scrapy.Request(url=douban_start_url,callback=self.parse_dbSearch)#必须要用yield而不能用return
        douban_moviedetail_url = 'https://movie.douban.com/subject/4920389/?from=showing'
        yield scrapy.Request(url = douban_moviedetail_url,callback = self.parse_dbMoviedetail)

      
        ''' 新浪微博爬虫初始URL '''
        #微博话题关键词，使用经过编码之后的字符串而不是中文
        keyword = "%E5%A4%B4%E5%8F%B7%E7%8E%A9%E5%AE%B6"
        #爬取100页的微博
        for page in range(1,100):
            yield Request(url="https://weibo.cn/search/mblog?hideSearchFrame=&keyword="+keyword+"&advancedfilter=1&hasori=1&sort=time&page=" +str(page), callback=self.parse_WeiBotopicSearch)
    

        ''' 时光网爬虫初始URL '''
        mhost = 'http://movie.mtime.com/'
        movie_id = '225925' # 这是“狂暴巨兽”这部电影的id，不同的电影id不同
        # 提取出代表页面的不同部分，使得构建下一页的url更方便
        # 这里出现了一个失误。。解析网页的时候发现其实下一页的按钮可以直接跳转到下一页页面，这个分割没什么作用
        middle_url_part = "/reviews/short/new"
        end_url_part = '.html'
        # 这是短评的第一页url，处理完之后进入下一页
        mtime_comment_url = mhost + movie_id + middle_url_part + end_url_part
        yield Request(url= mtime_comment_url, callback=self.parse_mtime_comment)

    ''' 时光网评论相应处理函数 '''
    def parse_mtime_comment(self,response):
        # print(response.text)

        # 通过xpth定位全部短评
        for each_comment in response.xpath('//div[@class="mod_short"]'):
            item = MtimescrapyItem()

            # 电影的名称
            movie = response.xpath('//*[@id="db_sechead"]/div[2]/div/h1/a/text()').extract()[0]

            # 电影的评论
            comment = each_comment.xpath('.//h3/text()').extract()[0]

            # 电影的评分
            scorexpath = each_comment.xpath('.//span[@class="db_point ml6"]/text()').extract()
            if scorexpath and scorexpath[0]:
                score=scorexpath[0]
            else:
                score=-1#-1代表没有打分

            # 这条评论的时间，但这个应该是js动态加载的，但不知道为什么可以直接被解析出来
            time = each_comment.xpath('.//div[@class="mt10"]/a/@entertime').extract()[0]

            # print(movie + '/t' + comment + '/t' + score + '\n')

            item['movie'] = movie
            item['comment'] = comment
            item['score'] = score
            item['time'] = time

            
            #positive, negative = wzAPI(comment)
            positive=1
            negative=1

            item['positive'] = positive
            item['negative'] = negative
            
            yield item



        # 判断还有没有下一页，没有下一页时网页的属性值是mr10 false，有的话是ml10 next，不过这里好像出了点问题。。。代码段没有执行，后续要填坑
        #已修复
        nextpage = response.xpath('//div[@id="PageNavigator"]/a[@class="ml10 next"]')
        print(nextpage)
        if nextpage:
            next_url=nextpage.xpath('./@href').extract()[0]
            print(next_url)
            yield Request(next_url, callback=self.parse_mtime_comment)
            
        else:
            pass
       


    ''' 豆瓣电影评论响应处理函数 '''
    def parse_dbSearch(self,response):
            scrapydoubanItem=DBScrapyItem()
            selector = Selector(response)
            divs = selector.xpath('//div[@class="comment"]')
            div =divs[0]
            useful_counts=div.xpath('//div[@class="comment"]//span[@class="comment-vote"]/span[@class="votes"]/text()').extract()
            usernames=div.xpath('//div[@class="comment"]//span[@class ="comment-info"]/a/text()').extract()
            userlinks=div.xpath('//div[@class="comment"]//span[@class ="comment-info"]/a/@href').extract()
            comment_times= div.xpath('//div[@class="comment"]//span[@class ="comment-info"]/span[@class="comment-time "]/@title').extract()
            comments= div.xpath('//div[@class="comment"]//p[@class=""]//text()').extract()
            attrindex=0
            for div in divs:
                scrapydoubanItem['useful_count'] = useful_counts[attrindex]
                scrapydoubanItem['username'] = usernames[attrindex]
                scrapydoubanItem['userlink'] = userlinks[attrindex]
                scrapydoubanItem['comment_time'] = comment_times[attrindex]
                scrapydoubanItem['comment'] =comments[attrindex]
                attrindex=attrindex+1
                yield scrapydoubanItem#请记得每次都要yeild这个item出去，否则你会发现没有数据没有保存
            #查找下一页
            nextpage_urls = selector.xpath('//div[@id="paginator"]/a[@class="next"]/@href').extract()
            for nextpage in nextpage_urls:
                yield Request(url = 'https://movie.douban.com/subject/4920389/comments'+nextpage,callback = self.parse_dbSearch)#将下一页的URL发送到scrapy待爬队列
        
    ''' 豆瓣电影详情页响应参数 '''
    def parse_dbMoviedetail(self,response):
        selector = Selector(response)
        with open('./data/moviedetail.txt','a+')as f:
            title = selector.xpath('//span[@property="v:itemreviewed"]//text()').extract()
            score = selector.xpath('//div[@class="rating_self clearfix"]/strong/text()').extract()
            vote_count=selector.xpath('//div[@class="rating_self clearfix"]//a[@class="rating_people"]//text()').extract()
            rating_weights=selector.xpath('//div[@class="ratings-on-weight"]/div[@class="item"]')
            f.write("电影名称:"+title[0]+'\n'+"电影评分:"+score[0]+'\n'+"评分人数:"+vote_count[0]+'\n')            
            rate_title = rating_weights[0].xpath('//span[starts-with(@class,"stars")]/text()').extract()
            rate_per = rating_weights[0].xpath('//span[@class="rating_per"]/text()').extract()
            rate_titles=[]
            for rate in rate_title:
                rate = re.findall('(\d)星',rate)[0]
                rate_titles.append(rate+'星')
            for i in range(0,5):
                f.write(rate_titles[i] +':'+rate_per[i]+'\n')
            betterthan = ' '.join(selector.xpath('//div[@class="rating_betterthan"]//text()').extract())
            f.write(betterthan)
            f.write('------------------>  update at '+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
            
            
    ''' 微博话题搜索响应结果处理函数 '''
    def parse_WeiBotopicSearch(self,response):
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
                #print('topic:'+tweet_contents.replace(u"\xa0", ""))
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
            
  