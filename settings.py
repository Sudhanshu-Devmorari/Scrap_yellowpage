DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ROTATING_PROXY_LIST = [line.strip() for line in open('proxies.txt') if line.strip()]

# DOWNLOADER_MIDDLEWARES = {
#     'yellowpages_scraper.middlewares.CustomProxyMiddleware':1,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':100,
# }