# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json

'''
Don't Use this proxy spider if you are not in China
scrapy crawl xici_proxy
''' 
class XiciSpider(scrapy.Spider):
    name = "xici_proxy"
    allowed_domains = ["www.xicidaili.com"]
    
    # Overwrite Middleware settings, only enable minimum middlewares, disable retry, useragent, 
    # format error messages in a better way with ProcessAllExceptionMiddleware
    # ProcessAllExceptionMiddleware Inspired by 
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'knowsmore.middlewares.ProcessAllExceptionMiddleware': 120,  
        }
    }

    def start_requests(self):
        for i in range(1, 4):
            yield Request('https://www.xicidaili.com/nn/%s' % i)
            yield Request('https://www.xicidaili.com/nt/%s' % i)
            yield Request('https://www.xicidaili.com/wn/%s' % i)
            yield Request('https://www.xicidaili.com/wt/%s' % i)

    def parse(self, response):
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            # extract IP、 port、 scheme(http or https)
            ip = sel.css('td:nth-child(2)::text').extract_first()
            port = sel.css('td:nth-child(3)::text').extract_first()
            scheme = sel.css('td:nth-child(6)::text').extract_first()
            if ip and port and scheme :
                scheme = scheme.lower()
                # Send request with proxy setting to http(s)://httpbin.org/ip
                url = '%s://httpbin.org/ip' % scheme
                proxy = '%s://%s:%s' % (scheme, ip, port)
                # print proxy
                meta = {
                    'proxy': proxy,
                    'dont_retry': True,
                    'download_timeout': 5,                    
                    '_proxy_scheme': scheme,
                    '_proxy_ip': ip,
                } 
                yield Request(url, callback=self.check_available, meta=meta, dont_filter=True)

    def check_available(self, response):
        if not response.url:
            pass
        elif 'exception' in response.url:
            pass
        else :
            proxy_ip = response.meta['_proxy_ip']
            if json.loads(response.text)['origin']:
                yield {
                    'proxy_scheme': response.meta['_proxy_scheme'],
                    'proxy': response.meta['proxy'],
                }

