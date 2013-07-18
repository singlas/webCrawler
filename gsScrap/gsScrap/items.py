# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class gsScrapItem(Item):
    Title = Field()
    URL = Field()
    GA = Field()
    Universal_Analytics = Field()
    GA_Remarketing = Field()
    Google_AdWords = Field()
    GA_Steroids = Field()
    Google_Tag_Manager = Field()

