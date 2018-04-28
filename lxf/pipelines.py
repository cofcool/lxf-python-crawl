# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class LxfPipeline(object):

    DIR_PREFIX = 'site'

    def __init__(self):
        if not os.path.isdir(LxfPipeline.DIR_PREFIX):
            os.mkdir(LxfPipeline.DIR_PREFIX)

        self.f = open(LxfPipeline.DIR_PREFIX + os.path.sep + 'titles.md', 'w')
        self.f_con = open(LxfPipeline.DIR_PREFIX + os.path.sep + 'contents' + '.md', 'w')

    def process_item(self, item, spider):
        if len(item['content']) == 0:
            self.parse_item(item['subMenus'][0])
        else:
            self.write_content(item['content'])

        return item

    def parse_item(self, item):
        topMenu = self.parse_level(item['level']) + ' ' + item['menuname'].encode('utf-8') + '\n'
        self.f.write(topMenu)

        for subMenu in item['subMenus']:
            self.parse_item(subMenu)

    def parse_level(self, level):
        levelStr = '#'
        for l in range(int(level)):
            levelStr = levelStr + '#'

        return levelStr;

    def write_content(self, content):
        self.f_con.write(content.encode('utf-8'))

    def close_spider(self, spider):
        self.f_con.close()
        self.f.close()
