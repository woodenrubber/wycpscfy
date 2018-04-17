# encoding=utf-8
# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------


from Spyder import items 
import time

class MyPipeline(object):
    
    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理 """
        if isinstance(item,items.Topic_TweeetItem):
            with open('./data/weiboData.txt','a+') as f:
                f.write(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+':'+'('+str(item['Nickname'])+','+item['UserLink']+','+item['Content']+','+str(item['LikeNum'])+','+str(item['RetweetNum'])+','+str(item['CommentNum'])+','+item['Source']+')'+'\n')
                #print('get topic search content:'+item['Content'])
        
        elif isinstance(item,items.DBScrapyItem):
            with open('./data/doubanData.txt','a+') as f:
                f.write(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+':'+'('+item['username']+','+item['userlink']+','+item['comment_time']+','+str(item['useful_count'])+','+item['comment']+')'+'\n')
        
        elif isinstance(item,items.MtimescrapyItem):
            with open('./data/mtimeData.txt','a+') as f:
                f.write(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+':'+item['movie']+','+item['comment']+','+str(item['score'])+','+item['time']+','+str(item['positive'])+','+str(item['negative'])+')'+'\n')
        return item
    

