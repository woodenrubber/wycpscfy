from QcloudApi.qcloudapi import QcloudApi
import ssl

def wzAPI(comment):
    # 使用腾讯文智自然语言处理，这部分代码本来按照规范应该写到pipelines.py里面的。。结果不知道为啥子一直不执行。。后续要填坑

    try:
        ssl._create_default_https_context = ssl._create_unverified_context  # 这一行是为了不让其验证自签名的证书，避免报错

        '''
        设置需要加载的模块
        '''
        module = 'wenzhi'

        '''
        action: 对应接口的接口名
        '''
        action = 'TextSentiment'

        '''
        config: 云API的公共参数
        '''
        config = {
            'secretId': 'AKIDdaXQSNUiAahrupg8f1EcDg1ODuQqxhux',
            'secretKey': '8VmIl4MkWEmlhUByhWg7cMYqDf6WMFTk',
            'Region': 'gz',
            'method': 'GET'
        }

        '''
                    接口参数
                    '''
        params = {"content": comment}  # 这里需要考虑如何将豆瓣的评论传入到其中，因为豆瓣的评论爬取出来是不规则的

        service = QcloudApi(module, config)

        # print(service.generateUrl(action, params))  # 这段可以不print出来

        wzResult = eval(service.call(action, params))  # 调用API，并将字符串结果用eval函数转换为字典

        '''
        分别得到正向情感和负向情感的值
        '''
        positive = wzResult["positive"]
        negative = wzResult["negative"]
        #
        # print(positive)
        # print(negative)

        return positive, negative

    except Exception as e:
        import traceback
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        return None, None