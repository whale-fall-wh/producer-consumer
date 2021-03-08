from producers.BaseProducer import BaseProducer
import schedule


class ProductProducer(BaseProducer):
    job_key = 'product_asin'  # 注意和消费者对应

    def __init__(self):
        schedule.every(10).seconds.do(self.start)
        BaseProducer.__init__(self)

    def start(self):
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
            self.set_job(asin_str)

