from flask import Flask, render_template
from subprocess import call

app = Flask(__name__)

@app.route("/")
def hello():
	domain = 'www.sidestix.com' 
    call("scrapy crawl gaScrap -a domain='%s' -o 'static/%s.json' -t json" % ( domain, domain), shell=True)
    entries = { 'aa':'bb', }
    return render_template('home.html', entries=entries)

if __name__ == "__main__":
    app.run(debug=True)