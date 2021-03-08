import common
from utils.Logger import Logger
from utils.Http import Http
import requests
from crawlers.elements.ProductTitle import get_title


class ProductCrawler:
    base_url = 'https://www.amazon.com/dp/{}'

    def __init__(self, asin: str):
        self.asin = asin
        self.url = self.base_url.format(self.asin)

    def run(self, http: Http):
        try:
            Logger().debug('开始抓取{}产品，地址 {}'.format(self.asin, self.url))
            rs = http.get(url=self.url, timeout=10)
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
        'B07214SKYV',
        'B072JMFRKQ',
        'B078NLCPYW',
        'B07BWPNMCB',
        'B075DGQWZT',
        'B077JYGQZ1',
        'B071WPR3FC',
        'B07TWPMZFF',
        'B07TYPP711',
        'B085Q2NVN8',
        'B074PLWQY3',
        'B077JYR2M2'
    ]
    for asin_str in asin_map:
        ProductCrawler(asin_str).run(Http())
        common.sleep_random()
