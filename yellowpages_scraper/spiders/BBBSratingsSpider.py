import scrapy, json
from pymongo import MongoClient
from bson.objectid import ObjectId

class BBBSratingsSpider(scrapy.Spider):
    name = 'bbb_ratings'
    allowed_domains = ['bbb.org']

    client = MongoClient('mongodb://localhost:27017/')
    database = client['hyper_local']
    collection = database['core_details']
    # collection.drop_index('__primary_key__')

    def start_requests(self):
        with open('output__04.json','r') as f:
            data = f.read()
        data = json.loads(data)
        print("++++++++", len(data))

        headers = {
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
             "Accept-Encoding": "gzip, deflate, br",
             "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
             "Connection": "keep-alive",
             "Cookie": "iabbb_session_id=d3513175-63d3-4668-af34-96c0d84d5d7c; AMCV_CB586B8557EA40917F000101%40AdobeOrg=179643557%7CMCIDTS%7C19488%7CMCMID%7C80930777511020490323312270326354457865%7CMCAAMLH-1684300433%7C12%7CMCAAMB-1684300433%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1683702834s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19495%7CvVersion%7C5.5.0; AMCVS_CB586B8557EA40917F000101%40AdobeOrg=1; _gcl_au=1.1.2062645814.1683695634; _ga=GA1.1.717072791.1683695634; s_nr30=1683698190389-New; s_ips=816; s_tp=4980; gpv_PageUrl=https%3A%2F%2Fwww.bbb.org%2Fsearch%3Ffind_country%3DUSA%26find_latlng%3D33.518838%252C-112.086005%26find_loc%3DPhoenix%252C%2520AZ%26find_text%3DInvestment%2520Management%26page%3D8%26sort%3DDistance; s_cc=true; s_sq=%5B%5BB%5D%5D; iabbb_ccpa=true; _gid=GA1.2.1295333142.1683698190; GA1.2.717072791.1683695634; _fbp=fb.1.1683695635571.1359295206; __gads=ID=f244a2738078b8e7:T=1683695636:S=ALNI_Madq6SOVmcu4REp83vWDv2-lk9Dow; __gpi=UID=00000c03ea22b487:T=1683695636:RT=1683695636:S=ALNI_MY1p6-MYykuKgTwFBNk8BdhxDY3XQ; iabbb_find_location=Phoenix%20AZ%20USA; _ga_PKZXBXGJHK=GS1.1.1683695644.1.1.1683698189.41.0.0; iabbb_user_culture=en-us; iabbb_user_location=Cordelia%2520CA%2520USA; iabbb_user_bbb=1116; iabbb_find_location=Phoenix%2520AZ%2520USA; iabbb_user_postalcode=94534; iabbb_accredited_search=true; iabbb_accredited_toggle_state=seen; _ga_MJQ72F5ZG5=GS1.1.1683696179.1.1.1683696638.0.0.0; bbbBureauId=1292; bbbCampaignId=49665; bbbVideoClipId=345; bbbTobId=20013-300; _gat_local=1; _gat_gtag_UA_41101326_21=1; _ga_MP6NWVNK4P=GS1.1.1683695633.1.1.1683698190.0.0.0; s_ppv=search%2520results%2520%257C%2520search%2C16%2C16%2C816%2C1%2C6",
             "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
             "sec-ch-ua-mobile": "?0",
             "Host": "www.bbb.org",
             "Sec-Fetch-Dest": "document",
             "Sec-Fetch-Mode": "navigate",
             "Sec-Fetch-Site": "none",
             "Sec-Fetch-User": "?1",
             "TE": "trailers",
             "Upgrade-Insecure-Requests": "1",
             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"
        }


        for business in data:
            business_name = business['name'].replace(" ", "%20")
        #     print("***********", business_name)
        #     # https://www.bbb.org/search?find_text=Essential%20Investing&find_loc=Phoenix%2C+AZ&page=1
            search_url = f"https://www.bbb.org/search?find_text={business_name}&find_loc={business['city']}%2C+{business['state']}&page=1"
            print("***********", search_url)
            yield scrapy.Request(search_url, headers=headers, callback=self.parse, meta={'business':business})
        # search_url = "https://www.bbb.org/search?find_text=Essential%20Investing&find_loc=Phoenix%2C+AZ&page=1"
        # print("***********", search_url)
        # yield scrapy.Request(url = search_url, callback=self.parse)

    # def parse_search_results(self, response):
    #     business = response.meta['business']
    #     result = response.css('.dtm-search-result-title a::attr(href)').get()

    #     if result:
    #         yield response.follow(result, callback=self.parse_business_details, meta={'business': business})

    def parse(self, response):
        print("--------------", response)
        # soup=BeautifulSoup(response.text, 'html.parser')
        # # print("++++++++++++++",soup)
        # with open('data.html','w') as f:
        #     f.write(str(soup))

        # rate = soup.find_all('div', {'class': 'MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation1 MuiCard-root result-item-ab exws2cl0 css-1iq30ye'})
        # for rt in rate:
        #     print("____________", rt)
        rating = response.css('div.result-item-ab.exws2cl0.css-1iq30ye span.bds-body::text').getall()
        print('======', rating[-1])
        # rating_text = rating.strip() if rating else ""
        # print("Rating:", rating_text)

        # rating = response.css('.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.MuiCard-root.result-item-ab.exws2cl0.css-1iq30ye').getall()
        # # print("+++++++++++", rating)
        # for bbb in rating:
        #     selector = scrapy.Selector(text=bbb)
        #     rate = selector.css('div.stack.css-mpye1m.eya12jt0 div.cluster span.bds-body::text').get()
        #     print("+++++++++++", rate)

        business = response.meta['business']
        business['bbb_rating'] = rating[-1]
        business['id'] = str(ObjectId())
        self.collection.insert_one(business)
        yield business















# L Roy Papp & Associates LLP:  A+
# Versant Capital Management Inc:  A+
# Westmark Wealth Management:  A+
# Taylor Street Property Management:  A
# CUE Financial Group Inc:  A+
# North Star Resource Group:  A+
# SGI Property Management Phoenix:  A+
# Rusk Investments Inc:  A+