# encoding=utf-8
# ------------------------------------------
#   版本：4.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

from scrapy import Item, Field



class Topic_TweeetItem(Item):
    """ 话题搜索微博内容 """
    Nickname = Field()
    UserLink = Field()
    Content = Field()
    LikeNum = Field()
    RetweetNum = Field()
    CommentNum = Field()
    Source = Field()
    
    
class DBScrapyItem(Item):
    ''' 豆瓣电影评论内容 '''
    username = Field()
    userlink = Field()
    comment_time = Field()
    useful_count = Field()
    comment = Field()
    
class MtimescrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 电影名称
    movie = Field()

    # 电影评论
    comment = Field()

    # 电影评分
    score = Field()

    # 评论的时间
    time = Field()

    # 正向的情感
    positive = Field()

    # 负向的情感
    negative = Field()
