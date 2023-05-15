import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import sys
import re, json

class yellowpagesNewSpider(CrawlSpider):
    name = 'yellowpagesNew'
    allowed_domains = ['yellowpages.com']

    def start_requests(self):
            with open('output__02.json','r') as f:
                data = f.read()
            data = json.loads(data)
            # print(data,'========')

            for i in range(len(data)):
                url = data[i]['url']
                print('URL:- ',url)
                yield scrapy.Request(url, callback=self.parse, meta={"keyword":data[i]['keyword'],"url":data[i]['url']})

    def extract_city_state_zip(self, locality_text):
        match = re.search(r"^(.*?),\s*(.*?),\s*([A-Z]{2})\s*(\d{5})$", locality_text)
        if match:
            address = match.group(1)
            city = match.group(2)
            state = match.group(3)
            postalcode = match.group(4)
            return address, city, state, postalcode
        else:
            try:
                data = re.search(r'([^<]+),\s*([^<]+)\s*(\d{5})', locality_text)
                address = None
                city = data.group(1)
                state = data.group(2)
                postalcode = data.group(3)
                return address,city, state, postalcode
            except:
                return None, None, None, None

    def parse(self, response):
        # print("=======response", response)
        # print("=======meta data", response.meta['keyword'])
        # print("=======categories: ", ', '.join(response.css('.categories .categories a::text').getall()).strip())
        locality_text = response.xpath('//section[@id="details-card"]/p[2]/text()').get()
        # print("=====",locality_text)
        address, city, state, postalcode = self.extract_city_state_zip(locality_text)
        # print("Address:", address)
        # print("City:", city)
        # print("State:", state)
        # print("Postal Code:", postalcode)
        # phone = response.css('a.phone.dockable strong::text').get()
        # print("+++++++++++", phone)
        email = response.css('a.email-business::attr(href)').get()
        if email:
            emails = email.split(':')[1]
        else:
            emails = None
        # print("+++++++++++", email.split(':')[1])
        # website = response.css('section.inner-section a:nth-child(2)::attr(href)').get()
        # rating = response.css('div.rating-stars::attr(class)').get().split(" ")[1]
        # business_year = response.css('div.years-in-business div.number::text').get()
        # print("+++++++++++website ", website)
        # print("+++++++++++rating ", rating)
        # print("+++++++++++business_year ", business_year)
        # review = response.css('a.yp-ratings.hasExtraRating span.count::text').get()
        # print("+++++++++++review ", review)
        # name = response.css('h1.dockable.business-name::text').get()
        # print("+++++++++++name ", name)
        # print("++++++++++1", response.xpath('//dd[@class="weblinks"]/p/a/text()').getall())
        # print("++++++++++2", response.xpath('//dd[@class="weblinks"]/p').getlist())
        # other_links = response.xpath('//dd[@class="weblinks"]/p/a/text()').getall()


        yield {
            'keyword': response.meta['keyword'],
            'categories': ', '.join(response.css('.categories .categories a::text').getall()).strip(),
            'name': response.css('h1.dockable.business-name::text').get(),
            'profile_url': response.meta['url'],
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postalcode,
            'phone': response.css('a.phone.dockable strong::text').get(),
            'email': emails,
            'website': response.css('section.inner-section a:nth-child(2)::attr(href)').get(),
            'rating': response.css('div.rating-stars::attr(class)').get().split(" ")[1],
            'review': response.css('a.yp-ratings.hasExtraRating span.count::text').get(),
            'years_in_business': response.css('div.years-in-business div.number::text').get(),
            'other_links': response.xpath('//dd[@class="weblinks"]/p/a/text()').getall()
        }









        # locality_text = response.css('.locality::text').get()
        # city, state, postal_code = self.extract_city_state_zip(locality_text)
        # yield{
        # # 'keyword' : response.css('input[name="search_terms"]::attr(value)').get(),
        # 'category': ', '.join(response.css('.categories a::text').getall()).strip(),
        # 'name': response.css('.business-name span::text').get(),
        # 'address': ' '.join(response.css('.street-address::text').getall()),
        # # 'city': city,
        # # 'state': state,
        # # 'postal_code': postal_code,
        # 'phone': response.css('.phones::text').get(),
        # 'email': response.css('.email-business a::attr(href)').re_first('mailto:(.*)'),
        # 'website': response.css('.links .track-visit-website::attr(href)').get(),
        # 'rating': response.css('.result-rating::attr(title)').get(),
        # 'business_year': response.css('.in-business::text').re_first('(\d+)'),
        # }






    # def __init__(self, *args, **kwargs):
    #     super(yellowpagesNewSpider, self).__init__(*args, **kwargs)
    #     self.keywords = kwargs.get('keywords', '').split(',')
    #     self.locations = [line.strip() for line in open('locations.txt') if line.strip()]
    #     self.start_urls = [f'https://www.yellowpages.com/search?search_terms={keyword.strip()}&geo_location_terms={location}' for keyword in self.keywords for location in self.locations]

    # rules = (
    #     Rule(LinkExtractor(restrict_css='.pagination a'), callback='parse_item', follow=True),
    # )

    # def extract_city_state_zip(self, locality_text):
    #     city_state_zip_pattern = re.compile(r'^(.*),\s+([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$')
    #     match = city_state_zip_pattern.match(locality_text)
    #     if match:
    #         return match.groups()
    #     else:
    #         return None, None, None
        
    # def parse_start_url(self, response):
    #     return self.parse_item(response)

    # def parse_item(self, response):
    #     text = response.text
    #     sel = scrapy.Selector(text=text)
    #     for business in sel.css('.result'):
    #         profile_url = business.css('.business-name a::attr(href)').get()
    #         if profile_url:
    #             yield response.follow(profile_url, callback=self.parse_business_details)

    # def parse_business_details(self, response):
    #     name = response.css('.sales-info h1::text').get()
    #     category = response.css('.business-categories a::text').get()
    #     address = ' '.join(response.css('.address .street-address::text').getall())
    #     city = response.css('.address .locality::text').get()
    #     state = response.css('.address .region::text').get()
    #     postal_code = response.css('.address .postal-code::text').get()
    #     phone = response.css('.phone::text').get()
    #     email = response.css('.email-business a::attr(href)').re_first('mailto:(.*)')
    #     website = response.css('.website-link a::attr(href)').get()
    #     rating = response.css('.rating span::text').get()
    #     reviews = response.css('.rating .count::text').get()
    #     year_in_business = response.xpath("//*[contains(text(), 'Years in Business')]/following-sibling::p/text()").get()

    #     item = {
    #         'keyword':response.css('input[name="search_terms"]::attr(value)').get(),
    #         'name': name,
    #         'category': category,
    #         'profile_url': response.url,
    #         'address': address,
    #         'city': city,
    #         'state': state,
    #         'postal_code': postal_code,
    #         'phone': phone,
    #         'email': email,
    #         'website': website,
    #         'rating': rating,
    #         'reviews': reviews,
    #         'year_in_business': year_in_business,
    #     }

    #     if website:
    #         yield scrapy.Request(website, callback=self.parse_website, meta={'item': item})
    #     else:
    #         yield item

    # def parse_website(self, response):
    #     item = response.meta['item']

    #     item['email_website'] = response.css('a[href^="mailto:"]::attr(href)').re_first('mailto:(.*)')
    #     item['phone_website'] = response.css('a[href^="tel:"]::attr(href)').re_first('tel:(.*)')
    #     item['facebook_website'] = response.css('a[href*="facebook.com"]::attr(href)').get()

    #     yield item
