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

    def process_item(self, item, spider):
        if len(item['content']) == 0:
            self.parse_item(item['subMenus'][0])
        else:
            self.write_content(self.get_name(item['menuHref']), item['content'])

        return item

    def parse_item(self, item):
        topMenu = self.parse_level(item['level'], item['menuname'].encode('utf-8'), item['menuHref'].encode('utf-8'))
        self.f.write(topMenu)

        for subMenu in item['subMenus']:
            self.parse_item(subMenu)

    def parse_level(self, level, menuname, menuHref):
        levelStr = '#'
        for l in range(int(level)):
            levelStr = levelStr + '#'

        return levelStr + ' [' + menuname + ']' + '(./' + self.get_name(menuHref) + '.md)\n';

    def get_name(self, url):
        return url.split('/')[-1]

    def write_content(self, filename, content):
        f_con = open(LxfPipeline.DIR_PREFIX + os.path.sep + filename + '.md', 'w')
        f_con.write(content.encode('utf-8'))
        f_con.close()

    def close_spider(self, spider):
        self.f.close()
