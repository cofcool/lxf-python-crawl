# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LxfItem(scrapy.Item):
    # define the fields for your item here like:
    menuname = scrapy.Field()
    menuHref = scrapy.Field()
    content = scrapy.Field()
    subMenus = scrapy.Field()
    level = scrapy.Field()
