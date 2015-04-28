# -*- coding: utf-8 -*-

# Scrapy settings for letmescrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'letmescrape'

SPIDER_MODULES = ['letmescrape.spiders']
NEWSPIDER_MODULE = 'letmescrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'letmescrape (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'letmescrape.pipelines.RequiredFieldsPipeline': 300,
}


########## ScrapyJS CONFIGURATION
# See : https://github.com/scrapinghub/scrapyjs
SPLASH_URL = 'http://192.168.59.103:8050'
DOWNLOADER_MIDDLEWARES = {
    'scrapyjs.SplashMiddleware': 725,
}
DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapyjs.SplashAwareFSCacheStorage'
########## END ScrapyJS CONFIGURATION