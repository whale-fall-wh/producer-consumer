import common
from utils.Logger import Logger
from utils.Http import Http
import requests
from crawlers.elements.ProductTitle import get_title
from crawlers.BaseAmazonSpider import BaseAmazonSpider


class ProductCrawler(BaseAmazonSpider):
    base_url = 'https://www.amazon.com/dp/{}'

    def __init__(self, asin: str, http: Http):
        self.asin = asin
        self.url = self.base_url.format(self.asin)
        BaseAmazonSpider.__init__(self, http=http)

    def run(self):
        try:
            Logger().debug('开始抓取{}产品，地址 {}'.format(self.asin, self.url))
            rs = self.get(url=self.url, timeout=10)
            title = get_title(rs.text)
            if title:
                Logger().info(title)
            else:
                Logger().error(self.asin + '抓取失败，' + '地址 ' + self.url)
        except requests.exceptions.RequestException:
            Logger().error(self.url + '超时')
            # 超时异常处理, 切换代理，并将任务重新放回队列


if __name__ == '__main__':
    asin_map = [
        'B01NAWKYZ0',
        'B01NAWKYZ0',
        'B01NAWKYZ0',
        'B01NAWKYZ0',
    ]
    new_http = Http()
    for asin_str in asin_map:
        ProductCrawler(asin_str, new_http)
        common.sleep_random()
