import json
import itertools

import scrapy
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider


class UrlSpider(scrapy.Spider):

    name = 'e27_urls'

    def start_requests(self):
        base_url = 'https://e27.co/startups/'
        payload = 'load_startups_ajax?per_page={}&append=1'
        for i in itertools.count(1):
            url = base_url + payload.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        html = json.loads(response.body)['pagecontent']
        doc = Selector(text=html)
        urls = doc.xpath(
            '//div[@class="col-xs-12 col-sm-12 col-md-4 col-lg-4"]/a/@href'
        )
        for u in urls.extract():
            yield {'url': u}

        if 'alert alert-danger no-margin' in html:
            raise CloseSpider('No page content found')
