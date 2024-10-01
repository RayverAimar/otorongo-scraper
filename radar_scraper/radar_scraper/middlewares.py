# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

class RadarScraperSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RadarScraperDownloaderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)

from scrapy.dupefilters import RFPDupeFilter
import logging

class CandidateDupeFilter(RFPDupeFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duplicated_requests = {}
        
    def request_seen(self, request):
        is_duplicate = super().request_seen(request)
        if is_duplicate:
            referrer = request.headers.get('Referer', 'No Referer').decode('utf-8')
            self.duplicated_requests[request.url] = referrer
        return is_duplicate
    
    def close(self, reason):
        if self.duplicated_requests:
            with open('duplicated_requests.txt', 'w') as f:
                for url, referer in self.duplicated_requests.items():
                    f.write(f"Duplicated URL: {url} from: {referer}\n")
        super().close(reason)
        
from urllib.parse import urlencode
from random import randint
import requests

class ScrapeOpsFakeBrowserMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_ENDPOINT')
        self.scrapeops_fake_browsers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_ENABLED')
        self.scrapeops_num_results = settings.get('SCRAPE_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browsers_enabled()
    
    def _get_headers_list(self):
        payload = {'api_key' : self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.browsers_list = json_response.get('result', [])
    
    def _get_random_browser_header(self):
        random_index = randint(0, len(self.browsers_list) - 1)
        return self.browsers_list[random_index]
    
    def _scrapeops_fake_browsers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '':
            self.scrapeops_fake_browsers_active = False
        else:
            self.scrapeops_fake_browsers_active = True
    def process_request(self, request, spider):
        random_header = self._get_random_browser_header()
        
        request.headers['user-agent'] = random_header['user-agent']
        request.headers['accept-language'] = random_header['accept-language']
        request.headers['accept'] = random_header['accept']
        request.headers['sec-ch-ua'] = random_header['sec-ch-ua']
        request.headers['sec-ch-ua-mobile'] = random_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua-platform'] = random_header['sec-ch-ua-platform']
        request.headers['sec-fetch-site'] = random_header['sec-fetch-site']
        request.headers['sec-fetch-mod'] = random_header['sec-fetch-mod']
        request.headers['sec-fetch-user'] = random_header['sec-fetch-user']
        request.headers['accept-encoding'] = random_header['accept-encoding']
        request.headers['accept-language'] = random_header['accept-language']
        request.headers['upgrade-insecure-requests'] = random_header['upgrade-insecure-requests']

import logging

class ErrorLoggingMiddleware:
    def __init__(self):
        self.error_urls = set()

    def process_response(self, request, response, spider):
        if response.status >= 400:
            self.error_urls.add(request.url)
        return response

    def process_exception(self, request, exception, spider):
        self.error_urls.add(request.url)
        return None

    def close_spider(self, spider):
        with open('error_urls.txt', 'w') as f:
            for url in self.error_urls:
                f.write(url + '\n')
        spider.logger.info(f"URLs with errors have been saved in 'error_urls.txt'")