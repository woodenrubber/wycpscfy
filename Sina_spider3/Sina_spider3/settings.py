# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

BOT_NAME = ['Sina_spider3']

SPIDER_MODULES = ['Sina_spider3.spiders']
NEWSPIDER_MODULE = 'Sina_spider3.spiders'

DOWNLOADER_MIDDLEWARES = {
    "Sina_spider3.middleware.UserAgentMiddleware": 401,
    "Sina_spider3.middleware.CookiesMiddleware": 402,
    "Sina_spider3.middleware.ProxyMiddleware":405,
}
ITEM_PIPELINES = {
    "Sina_spider3.pipelines.MyPipeline": 403,
}
DEPTH_LIMIT=10#The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
DEPTH_PRIORITY=1#0:所有深度的请求都会平等处理 大于0：先处理深度低的请求 小于0：先处理深度高的请求
DOWNLOAD_DELAY = 0.25  # 间隔时间 单位：秒
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 32  # 默认为16
CONCURRENT_ITEMS = 100
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = False
