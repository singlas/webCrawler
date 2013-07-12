import sys, os
import logging

os.chdir("/home/gitcode/webCrawler/gsScrap")
sys.path.append('/home/gitcode/webCrawler/gsScrap')
logging.basicConfig(stream=sys.stderr)

from home import app as application
