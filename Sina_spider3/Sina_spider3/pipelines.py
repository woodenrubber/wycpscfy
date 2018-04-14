# encoding=utf-8
# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------


from Sina_spider3 import items 


class MyPipeline(object):
    
    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理 """
        if isinstance(item, items.RelationshipsItem):
            with open('/usr/apps/sinaspider/relationshipData.txt','a') as f:
                f.write(item["followID"]+',')
                #print('get followed user id:'+str(item['followID']))
           
        elif isinstance(item, items.TweetsItem):
            with open('/usr/apps/sinaspider/tweetsData.txt','a') as f:
                f.write('('+str(item['_id'])+','+str(item['ID'])+','+item['Content']+','+str(item['PubTime'])+','+item['Co_oridinates']+','+str(item['Tools'])+','+str(item['Like'])+','+str(item['Comment'])+','+str(item['Transfer'])+')'+'\n')
                #print('content:'+item['Content'])
           
        elif isinstance(item, items.InformationItem):
            with open('/usr/apps/sinaspider/informationData.txt','a') as f:
                f.write('('+str(item['_id'])+','+item['NickName']+','+item['Gender']+','+item['Province']+','+item['City']+','+item['BriefIntroduction']+','+str(item['Birthday'])+','+str(item['Num_Tweets'])+','+str(item['Num_Follows'])+','+str(item['Num_Fans'])+','+item['SexOrientation']+','+str(item['Sentiment'])+','+item['VIPlevel']+','+item['Authentication']+','+item['URL']+')'+'\n')
                #print('get user info:'+item['NickName'])
        elif isinstance(item,items.Topic_TweeetItem):
            with open('/usr/apps/sinaspider/topicData.txt','a+') as f:
                f.write('('+str(item['Nickname'])+','+item['UserLink']+','+item['Content']+','+str(item['LikeNum'])+','+str(item['RetweetNum'])+','+str(item['CommentNum'])+','+item['Source']+')'+'\n')
                #print('get topic search content:'+item['Content'])
        return item
    

