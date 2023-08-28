import scrapy

from steamgames.items import BestbuyItem, clean_permonth, clean_offer_percent, clean_regular_price, clean_color, clean_for_months
from scrapy_playwright.page import PageMethod


class BestbuyComSpider(scrapy.Spider):
    name = 'bestbuy.com'
    allowed_domains = ['bestbuy.com']
    start_urls = ['http://bestbuy.com/']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'bestbuy.csv',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    def __init__(self, page='', keyword='', *args, **kwargs):
        super(BestbuyComSpider, self).__init__(*args, **kwargs)
        self.page = page
        self.keyword = keyword

        def start_requests(self):
        # arg = 'iphone'
        # page = 1
        url = f'https://www.bestbuy.com/site/searchpage.jsp?cp={self.page}&st={self.keyword}&intl=nosplash'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        with open('bestbuy.html', 'w') as f:
            f.write(response.text)
        products = response.xpath('//li[@class="sku-item"]')
        for product in products:

            data = product.xpath('.//div[@class="sku-list-item-price"]/div/div/script/text()').get()
            data = json.loads(data)
            price = data['app']['data']['customerPrice']
            if 'showPerMonth' in data['app']['data'] and data['app']['data']['showPerMonth'] is True:
                full_price = str(price) + '/Per Month'
            else:
                full_price = price

            title = product.xpath('.//h4/a/text()').get()
            # price = product.xpath('.//div[@class="priceView-hero-price priceView-customer-price"]/span[1]/text()').get()
            # print(price)
            # per_month = product.xpath(".//span[@class='priceView-subscription-units']/text()").get()
            # for_months = product.xpath(".//div[@class='priceView-price-disclaimer']").get()

            if 'regularPrice' not in data['app']['data']:
                regular_price = 'Not Given'
                offer_percent = 'Not Given'
            else:
                regular_price = data['app']['data']['regularPrice']
                offer_percent = price / regular_price * 100
                offer_percent = 100 - offer_percent
                offer_percent = round(offer_percent, 2)
                offer_percent = str(offer_percent) + '%'

            color = product.xpath(".//div[@class='product-variation-header']/div[2]/text()").get()
            model_number = product.xpath(".//div[@class='sku-model']/div/span[2]/text()").get()
            sku = product.xpath(".//div[@class='sku-model']/div[2]/span[2]/text()").get()
            if sku is None:
                sku = product.xpath(".//span[@class='sku-value']/text()").get()
            else:
                sku = sku
            image_url = product.xpath('.//img/@src').get()
            product_url = product.xpath('.//h4/a/@href').get()
            url = 'https://www.bestbuy.com' + product_url
            rating = product.xpath(".//p[@class='visually-hidden']/text()").get()

            # if per_month is None:
            #
            #     # Cleaning the data
            #     per_month = clean_permonth(per_month)
            #     # for_months_r = clean_for_months(for_months)
            #     offer_percent = clean_offer_percent(offer_percent)
            #     regular_price = clean_regular_price(regular_price)
            #     color = clean_color(color)
            #     full_price = str(price) + per_month #+ for_months_r
            #
            # else:
            #     full_price = price

            item = BestbuyItem()
            item['title'] = title
            item['price'] = full_price
            item['offer_percent'] = offer_percent
            item['regular_price'] = regular_price
            item['color'] = color
            item['model_number'] = model_number
            item['sku'] = sku
            item['image_url'] = image_url
            item['product_url'] = url
            item['rating'] = rating

            yield item