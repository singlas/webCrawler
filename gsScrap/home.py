from flask import Flask, render_template,request
from subprocess import call
import urllib2, StringIO, csv
import logging
from time import sleep 
import re   
from urllib2 import urlopen
from operator import itemgetter
from urlparse import urlparse


app = Flask(__name__)
file_handler = logging.FileHandler(filename='/tmp/webCrawler.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)

@app.route("/", methods=['GET','POST'])
def home():
    return render_template('home.html',itemcount= request.args.get('limit', '5000'))

@app.route('/result', methods=['GET','POST'])
def result():
    domain = request.args.get('domain')
    follow = request.args.get('follow')
    deny_url = request.args.get('deny_url')
    subdomains = request.args.get('subdomains')
    itemcount = request.args.get('itemcount')
    host ="gachecker.com" # "192.241.212.219"
    #host="localhost"
    msg_type = 'success'
    msg = "We just crawled <b>%s</b>" % domain
    display = 'block'    
    
    o=urlparse(domain)
    if(o.netloc==''):
        domain="http://" + domain

    try:
        domain = urlopen(domain).geturl()
    except urllib2.HTTPError, e:
        msg_type = 'error'
        msg = "<b>HTTP %d error on domain!</b> Please check the domain and try again" % e.code 
        display='none'
        return render_template('crawler.html', html="", domain=domain, type=msg_type, message=msg, display=display, link="#")

    o=urlparse(domain)
    csvfile = '/var/www/public/%s.csv' % o.netloc

    command = "rm -f %s & scrapy crawl gaScrap -a domain='%s' -a follow=%s -a deny_url=%s -a subdomains=%s -o %s -t csv --set CLOSESPIDER_ITEMCOUNT=%s" \
                 % ( csvfile, domain, follow, deny_url,subdomains, csvfile, itemcount ) 
    app.logger.info(command)   
    call(command, shell=True)
    
    url = 'http://%s/public/%s.csv' % ( host, o.netloc )
    response = urllib2.urlopen(url).read()
    output = StringIO.StringIO(response)
    cr = csv.reader(output)
    rowdata = []  

    for row in cr:
        size1 = len( row[0].split('.') )
        size2 = len( row[0].split('/') )
        row.append(size1)
        row.append(size2)
        rowdata.append(row)

    rowdata = sorted(rowdata, key=itemgetter(9,8,0))
    html = ""

    def format(x):
	    if(x=='0'):
	        return '<i class="icon-remove"></i>' 
	    elif(x=='1'): 
	        return '<i class="icon-ok"></i>'
	    else:
	        return str( x )

    for (i,row) in enumerate(rowdata):
    	row = map( format , row )
    	if (i!=0):
            html += "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( i, row[0], row[2],row[3],row[4],row[6],row[7] )    
    return render_template('crawler.html', html=html, domain=domain, type=msg_type, message=msg, display=display, link=url)

if __name__ == "__main__":
    app.run(debug=True)
