from crawlers.ProductSpilder import ProductCrawler
from utils.Logger import Logger
from utils.Http import Http
import common
from consumers.BaseConsumer import BaseConsumer


class ProductConsumer(BaseConsumer):
    # ignore = True     # 忽略该消费者
    job_key = 'product_asin'

    def run(self):
        Logger().info('product_consumer start')
        while True:
            asin_str = self.get_job()
            if asin_str:
                ProductCrawler(asin_str).run(Http())
                common.sleep_random()
            else:
                common.sleep(5)


if __name__ == '__main__':
    t = ProductConsumer()
    t.setDaemon(False)  # 非守护进程，主线程结束任务之后，会等待线程结束
    t.start()
