import random
import scrapy


class ProfileSpider(scrapy.Spider):

    name = 'e27_profiles'

    def start_requests(self):
        with open('urls.csv') as inf:
            urls = inf.read().split('\n')[1:-1]
        for url in random.sample(urls, 250):
            yield scrapy.Request(url=url + '?json', callback=self.parse)

    def parse(self, response):
        company_url = response.xpath('//div[@class="mbt"]/span[1]/a/text()')
        location = response.xpath('//div[@class="mbt"]/span[3]/a/text()')
        employee_range = response.xpath('//div[@class="row team"]')

        description = response.xpath(
            '//p[@class="profile-desc-text"]/text()'
        ).extract_first()
        description = description.strip() if description else ''

        company_name = response.xpath(
            '//h1[@class="profile-startup"]/text()'
        ).extract_first()
        company_name = company_name.strip() if company_name else ''

        tags = response.xpath(
            '//div[@style="word-wrap: break-word;"]/span/a/text()'
        )

        founding_date = response.xpath(
            "//p[contains(text(),'Founded')]/span/text()"
        )

        urls = response.xpath(
            '//div[@class="col-md-5 socials pdt text-right "]/a/@href'
        )

        description_short = response.xpath(
            '//h1[@class="profile-startup"]/following-sibling::div[1]/text()'
        )

        yield {
            'company_name': company_name,
            'request_url': response.url.rstrip('?json'),
            'request_company_url': company_url.extract_first(),
            'location': location.extract_first(),
            'tags': tags.extract(),
            'founding_date': founding_date.extract_first(),
            'founders': '',
            'employee_range': len(employee_range),
            'urls': urls.extract(),
            'emails': '',
            'phones': '',
            'description_short': description_short.extract_first(),
            'description': description
        }
