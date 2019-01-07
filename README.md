# knowsmore
A Spider system developed by Scrapy

This project is inspired by psn-price-tracker: [https://github.com/swnoh/psn-price-tracker/](https://github.com/swnoh/psn-price-tracker/)

## Prerequests

```
pip install scrapy_proxies
pip install fake_useragent
pip install mongoengine
pip install sqlalchemy

```

## Project Structure

PROJECT ROOT
	|- Knowsmore (folder)
		|- model (mongoengine and sqlalchemy ORM, used for DB storage, dont conflict with scrapy items)
		|- pipeline (diffed by mongoengine and sqlalchemy)
		|- spiders (scrapy spiders)
		|- common.py (some global helper functions)
		|- items.py (scrapy items)
		|- middlewares.py (random useragent and exception handling)
		|- pipelines.py (scrapy pipelines, entrance of pipeline folder, extra free proxy save handler)
		|- settings.py (scrapy settings)
	|- scrapy.cfg (with deploy info to scrapyd if possible)

## Scrapy Settings
```
DOWNLOADER_MIDDLEWARES = {
    'knowsmore.middlewares.RandomUserAgent': 1,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 80,    
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    ############################################################
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'knowsmore.middlewares.RandomHttpProxyMiddleware': None,
}

ITEM_PIPELINES = {
   'knowsmore.pipelines.MongoPipeline': 300,
   'knowsmore.pipelines.ProxySavePipeline': 299
   # 'knowsmore.pipelines.PsnSqlalchemyPipeline': 300,
}

RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RETRY_TIMES = 10

# Change this to wherever you project lies
PROXY_LIST = '/runtime/app/knowsmore/knowsmore/proxy_list.txt'
PROXY_MODE = 0

RANDOM_PROXY_SPIDER = ['xici_proxy']

# Used by Pipeline with model
STORAGE_TYPE = 'database'
DB_DRIVER = 'mongodb'
DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = 'YOUR DB NAME'
DB_USERNAME = ''
DB_PASSWORD = ''
```
## How it work
	|- Spider Send Requests
	|- || random useragent + random proxy
	|- \/ (middlewares)
	|- Yield Items
	|- || (scrapy items)
	|- \/
	|- Pipeline
	|- || 
	|- \/
	|- Model (MongoEngine or SQLAlchemy)

## Random Proxy
scrapy_proxies is used to deploy random proxy functinality for spider, all proxy data are crawled by spider => xici.py, inspired by an article from Internet, but I cannot find the original page, will add later if lucky, Please only use this spider in China coz the proxy site is not available abroad

