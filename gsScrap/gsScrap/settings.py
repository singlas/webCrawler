# Scrapy settings for gsScrap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'gsScrap'

SPIDER_MODULES = ['gsScrap.spiders']
NEWSPIDER_MODULE = 'gsScrap.spiders'

FEED_EXPORTERS = {
    'csv': 'gsScrap.feedexport.CSVkwItemExporter'
}

EXPORT_FIELDS = [
    'Title',
    'Link',
    'GA',
    'GA_Remarketing',
    'GA_Steroids',
    'Google_Addworks',     
    'Google_Tag_Manager',
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'gsScrap (+http://www.yourdomain.com)'
