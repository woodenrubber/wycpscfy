# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2018-4-05
#   作者：liwenbin
# ------------------------------------------

BOT_NAME = ['Spyder']

SPIDER_MODULES = ['Spyder.spiders']
NEWSPIDER_MODULE = 'Spyder.spiders'

DOWNLOADER_MIDDLEWARES = {
    "Spyder.middleware.UserAgentMiddleware": 401,
    "Spyder.middleware.CookiesMiddleware": 402,
    "Spyder.middleware.ProxyMiddleware":405,
}
ITEM_PIPELINES = {
    "Spyder.pipelines.MyPipeline": 403,
}
ROBOTSTXT_OBEY = False#遵守网站的robots.txt规则
DEPTH_LIMIT=0#The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed.
DEPTH_PRIORITY=1#0:所有深度的请求都会平等处理 大于0：先处理深度低的请求 小于0：先处理深度高的请求
DOWNLOAD_DELAY = 1  # 间隔时间 单位：秒
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 32  # 默认为16
CONCURRENT_ITEMS = 100
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = False
