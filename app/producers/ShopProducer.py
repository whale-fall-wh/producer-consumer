# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/29 11:24 上午 
# @Author : wangHua
# @File : ShopProducer.py 
# @Software: PyCharm


from app.producers import BaseProducer
from utils import Logger
from app.repositories import ShopItemRepository
from app.entities import ShopJobEntity as CurrentJobEntity
from app.enums import RedisListKeyEnum, ProductTypeEnum
from progress.bar import Bar


class ShopProducer(BaseProducer):

    def __init__(self):
        self.job_count = 0
        self.shopItemRepository = ShopItemRepository()
        BaseProducer.__init__(self)

    def set_job_key(self) -> str:
        return RedisListKeyEnum.shop_crawl_job

    def _schedule(self):
        # 每天凌晨执行任务
        self.schedule.every().day.at('00:00').do(self.start)

    def start(self):
        shopItems = self.shopItemRepository.all()
        if shopItems:
            with Bar('product-review-producer...', max=len(shopItems), fill='#', suffix='%(percent)d%%') as bar:
                for shopItem in shopItems:
                    shop = shopItem.shop
                    if shopItem.site:
                        entity = CurrentJobEntity.instance({
                            'shop_item_id': shopItem.id,
                            'shop_id': shop.id,
                            'shop_asin': shop.asin,
                            'site_id': shopItem.site.id,
                            'site_name': shopItem.site.name,
                            'page': 1
                        })
                        self.set_job(entity)
                        self.job_count += 1
                    bar.next()

        Logger().info('shop 开始投放任务,{}个产品, 共添加{}个任务'.format(len(shopItems), self.job_count))
