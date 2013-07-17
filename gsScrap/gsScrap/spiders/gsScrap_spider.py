from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from gsScrap.items import gsScrapItem
from scrapy.item import Item
import re

class gsScrapSpider(CrawlSpider):
    name = "gaScrap"        
    
    rules = ( Rule(SgmlLinkExtractor(),'parse_item', follow=True), ) 

    def __init__(self, domain=None, *a, **kw):
    	super(gsScrapSpider, self).__init__(*a, **kw)
        self.allowed_domains = ['%s' % domain ]
        self.start_urls = ['http://%s' % domain]        

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        item = gsScrapItem()
        item['URL'] = response.url
        item['Title'] = hxs.select('//title/text()').extract().pop().strip()   
        
        #_gaq.push(['_trackPageview']);
        gaq1 = hxs.select('//script/text()').re(r"_gaq\.push\( *\[ *\'_trackPageview\' *\] *\)")     
        #_gaq.push(['_setAccount', 'UA-XXXXX-Y']);    
        gaq2 = hxs.select('//script/text()').re(r"_gaq\.push\( *\[ *\'_setAccount\' *\, *'UA\-.*\-.*'*\] *\)")

        #gs.js
        gajs1 = hxs.select('//script/text()').re(r'ga\.js')  
        
        item['GA'] = len(gajs1) and len(gaq1) and len(gaq2)

        #dc.js
        dcjs1 = hxs.select('//script/text()').re(r'dc\.js')  
        item['GA_Remarketing'] = len(dcjs1) and len(gaq1) and len(gaq2)

        #var google_conversion_id = XXXXXXXXX;
        gaw1 = hxs.select('//script/text()').re(r"var * google_conversion_id *\= * \d+") 
        gaw2 = hxs.re(r'googleadservices\.com\/pagead\/conversion\.js' )
        item['Google_Addworks']= len(gaw1) and len(gaw2)

        #_gas.push(['_trackPageview']);
        gas1 = hxs.select('//script/text()').re(r"_gas\.push\( *\[ *\'_trackPageview\' *\] *\)")     
        #_gas.push(['_setAccount', 'UA-XXXXX-Y']);    
        gas2 = hxs.select('//script/text()').re(r"_gas\.push\( *\[ *\'_setAccount\' *\, *'UA\-.*\-.*'*\] *\)")
        #gas-1.10.1.min.js
        gasjs1 = hxs.select('//script/text()').re(r'gas.*\.js')  
        item['GA_Steroids'] = len(gasjs1) and len(gas1) and len(gas2)

        #www.googletagmanager.com/ns.html and
        gtm1 = hxs.re(r'googletagmanager\.com\/ns\.html') 
        #www.googletagmanager.com/gtm.js
        gtm2 = hxs.re(r'googletagmanager\.com\/gtm\.js') 
        item['Google_Tag_Manager'] = len(gtm1) and len(gtm2)
        return item

