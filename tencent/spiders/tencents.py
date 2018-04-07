# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencentpositionSpider(scrapy.Spider):
    name = "tencents"
    allowed_domains = ["tencent.com"]
    url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [url + str(offset)]


    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            # 初始化模型对象
            item = TencentItem()
            # 职位
            item['positionname'] = each.xpath("./td[1]/a/text()").get()
            # 详情连接
            hr_url = 'https://hr.tencent.com/'
            item['positionlink'] = hr_url + each.xpath("./td[1]/a/@href").get()
            # 职位类别
            item['positionType'] = each.xpath("./td[2]/text()").get()
            # 招聘人数
            item['peopleNum'] = each.xpath("./td[3]/text()").get()
            # 工作地点
            item['workLocation'] = each.xpath("./td[4]/text()").get()
            # 发布时间
            item['publishTime'] = each.xpath("./td[5]/text()").get()

            yield item
        if self.offset < 4010:
            self.offset += 10
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
