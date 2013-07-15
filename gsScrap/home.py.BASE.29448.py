from flask import Flask, render_template,request
from subprocess import call
import urllib2, StringIO, csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/result', methods=['GET','POST'])
def result():
    domain = request.args.get('domain')
    csvfile = '/var/www/public/%s.csv' % domain
    command = "rm %s & scrapy crawl gaScrap -a domain='%s' -o %s 	 -t csv" % ( csvfile, domain, csvfile)
    call(command, shell=True)

    url = 'http://localhost/public/%s.csv' % domain
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
	        return repr( x )

    for (i,row) in enumerate(cr):
    	row = map( format , row )
    	if (i!=0):
            html += "<tr><td>%d</td><td><a href='%s'>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( i, row[1], row[0], row[2],row[3],row[4],row[5],row[6] )    
    return render_template('crawler.html', html=html, domain=domain, link=url)

if __name__ == "__main__":
    app.run(debug=True)