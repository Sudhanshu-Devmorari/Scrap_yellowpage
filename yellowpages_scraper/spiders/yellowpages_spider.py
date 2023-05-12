import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
import re

class YellowPagesSpider(CrawlSpider):
    name = 'yellowpages'
    allowed_domains = ['yellowpages.com']

    def __init__(self, *args, **kwargs):
        super(YellowPagesSpider, self).__init__(*args, **kwargs)
        self.keywords = kwargs.get('keywords', '').split(',')
        self.locations = [line.strip() for line in open('locations.txt') if line.strip()]
        self.start_urls = [f'https://www.yellowpages.com/search?search_terms={keyword.strip()}&geo_location_terms={location}' for keyword in self.keywords for location in self.locations]

    rules = (
        Rule(LinkExtractor(restrict_css='.pagination a'), callback='parse_item', follow=True),
    )

    def extract_city_state_zip(self, locality_text):
        city_state_zip_pattern = re.compile(r'^(.*),\s+([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$')
        match = city_state_zip_pattern.match(locality_text)
        if match:
            return match.groups()
        else:
            return None, None, None

    def parse_item(self, response):
        keyword = response.css('input[name="search_terms"]::attr(value)').get()

        for business in response.css('.result'):
            relative_url = business.css('.business-name::attr(href)').get()
            profile = f'https://www.yellowpages.com{relative_url}'
            # business_url = business.css('.business-name a::attr(href)').get()
            # absolute_url = response.urljoin(business_url)
            locality_text = business.css('.locality::text').get()
            city, state, postal_code = self.extract_city_state_zip(locality_text)
            yield {
                'keyword': keyword,
                # 'category': ', '.join(business.css('.categories a::text').getall()).strip(),
                # 'name': business.css('.business-name span::text').get(),
                'profile_url': profile,
                # 'address': ' '.join(business.css('.street-address::text').getall()),
                # 'city': city,
                # 'state': state,
                # 'postal_code': postal_code,
                # 'phone': business.css('.phones::text').get(),
                # 'email': business.css('.email-business::attr(href)').re_first('mailto:(.*)'),
                # 'website': business.css('.links .track-visit-website::attr(href)').get(),
                # 'rating': business.css('.result-rating::attr(title)').get(),
                # 'business_year': business.css('.in-business::text').re_first('(\d+)'),
            }