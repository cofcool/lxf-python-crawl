# -*- coding: utf-8 -*-
import scrapy
from lxf.items import LxfItem

class LxfSpider(scrapy.Spider):
    name = 'python'
    allowed_domains = ['www.liaoxuefeng.com']
    start_urls = ['https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000']

    def parse(self, response):
        lxfItem = LxfItem()
        lxfItem['subMenus'] = []
        lxfItem['content'] = ''
        topLevel = response.xpath('//ul[@id="x-wiki-index"]')

        self.parse_menus(lxfItem, topLevel)

        links = []
        self.parse_links(lxfItem['subMenus'][0], links)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)

        yield lxfItem

    def parse_links(self, item, links):
        links.append(item['menuHref'].encode('utf-8'))
        for subMenu in item['subMenus']:
            self.parse_links(subMenu, links)

    def parse_menus(self, lxfItem, response):
        nextlevel = response.xpath('./div')
        for levelItem in nextlevel:
            subItem = LxfItem()
            subItem['subMenus'] = []
            subItem['content'] = ''
            subItem['level'] = levelItem.xpath('./@depth')[0].extract()
            subItem['menuname'] = levelItem.xpath('./a/text()')[0].extract()
            subItem['menuHref'] = "https://" + LxfSpider.allowed_domains[0] + levelItem.xpath('./a/@href')[0].extract()

            lxfItem['subMenus'].append(subItem)

            self.parse_menus(subItem, levelItem)

    def parse_content(self, response):
        contentStr = ''
        contents = response.xpath('//div[@class="x-wiki-content x-main-content"]/*/text()')
        for content in contents:
            contentStr = contentStr + content.extract() + '\n'

        lxfItem = LxfItem()
        lxfItem['content'] = contentStr
        lxfItem['menuHref'] = response.url

        yield lxfItem
