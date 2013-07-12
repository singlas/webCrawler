# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class gsScrapItem(Item):
    Title = Field()
    Link = Field()
    GA = Field()
    GA_Remarketing = Field()
    Google_Addworks = Field()
    GA_Steroids = Field()
    Google_Tag_Manager = Field()

