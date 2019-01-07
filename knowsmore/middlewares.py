# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict
import json
import random
from fake_useragent import UserAgent

from scrapy.http import HtmlResponse

class ProcessAllExceptionMiddleware(object):
    def process_response(self,request,response,spider):
        #捕获状态码为40x/50x的response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            print('Got status: %s' % (response.status))
            #随意封装，直接返回response，spider代码中根据url==''来处理response
            response = HtmlResponse(url='')
            return response
        #其他状态码不处理

        return response
    def process_exception(self,request,exception,spider):
        #在日志中打印异常类型
        print('Got exception: %s' % (exception))
        #随意封装一个response，返回给spider
        response = HtmlResponse(url='exception')
        return response

class RandomUserAgent(object):
    # def __init__(self,crawl):
    #     super(RandomUserAgent,self).__init__()
    #     self.ua=UserAgent()
    def process_request(self, request, spider):
        #useragent = random.choice(USER_AGENTS)
        ua = UserAgent()
        request.headers.setdefault("User-Agent",ua.random)

class KnowsmoreSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KnowsmoreDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='latin-1', proxy_list_file=None, spider = None):
        if not proxy_list_file:
            raise NotConfigured

        self.auth_encoding = auth_encoding
        # 分别用两个列表维护HTTP和HTTPS的代理， {'http': [...], 'https':
        self.proxies = defaultdict(list)
        self.spider = spider
        # 从json文件中读取代理服务器信息， 填入self.proxies
        fo = open(proxy_list_file, 'r')
        for line in fo.readlines():
            line = line.strip()
            proxy = json.loads(line)
            print proxy
            scheme = proxy['proxy_scheme']
            url = proxy['proxy']
            self.proxies[scheme].append(self._get_proxy(url, scheme))
        fo.close()

    @classmethod
    def from_crawler(cls, crawler):
        # 从配置文件中读取用户验证信息的编码
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','latin-1')
        # 从配置文件中读取代理服务器列表文件（json） 的路径
        proxy_list_file = crawler.settings.get('PROXY_LIST')
        return cls(auth_encoding, proxy_list_file, crawler.spider)
        
    def _set_proxy(self, request, scheme):
        if self.spider.name != 'xici_proxy':
            # 随机选择一个代理
            creds, proxy = random.choice(self.proxies[scheme])
            request.meta['proxy'] = proxy
            # print proxy
            if creds:
                request.headers['Proxy-Authorization'] = b'Basic ' + creds  

