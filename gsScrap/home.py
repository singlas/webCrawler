from flask import Flask, render_template,request
from subprocess import call
import urllib2, StringIO, csv
import logging
from time import sleep 
import re   
from urllib2 import urlopen


app = Flask(__name__)
file_handler = logging.FileHandler(filename='/tmp/webCrawler.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/result', methods=['GET','POST'])
def result():
    domain = request.args.get('domain')
    match = re.match( r'^(?=.{4,255}$)([a-zA-Z0-9][a-zA-Z0-9-]{,61}[a-zA-Z0-9]\.)+[a-zA-Z0-9]{2,5}$', domain )

    msg_type = 'success'
    msg = "We just crawled <b>%s</b>" % domain
    display = 'block'
    
    if( match == None ):
        msg_type = 'error'
        msg = "<b>Domain name not valid!</b> Please check the domain and try again"
        display='none'
        return render_template('crawler.html', html="", domain=domain, type=msg_type, message=msg, display=display, link="#")
    else:
        try:
            urlopen( 'http://' + domain)
        except urllib2.HTTPError, e:
            msg_type = 'error'
            msg = "<b>HTTP %d error on domain!</b> Please check the domain and try again" % e.code 
            display='none'
            return render_template('crawler.html', html="", domain=domain, type=msg_type, message=msg, display=display, link="#")
 
    follow = request.args.get('follow')
    deny_url = request.args.get('deny_url')
    csvfile = '/var/www/public/%s.csv' % domain
    command = "rm -f %s & scrapy crawl gaScrap -a domain='%s' -a follow=%s -a deny_url=%s -o %s -t csv" % ( csvfile, domain, follow, deny_url, csvfile )    
    call(command, shell=True)
    #
    url = 'http://192.241.212.219/public/%s.csv' % domain
    response = urllib2.urlopen(url).read()
    output = StringIO.StringIO(response)
    cr = csv.reader(output)

    html = ""

    def format(x):
	    if(x=='0'):
	        return '<i class="icon-remove"></i>' 
	    elif(x=='1'): 
	        return '<i class="icon-ok"></i>'
	    else:
	        return str( x )

    for (i,row) in enumerate(cr):
    	row = map( format , row )
    	if (i!=0):
            html += "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( i, row[0], row[2],row[3],row[4],row[5],row[6],row[7] )    
    return render_template('crawler.html', html=html, domain=domain, type=msg_type, message=msg, display=display, link=url)

if __name__ == "__main__":
    app.run(debug=True)
