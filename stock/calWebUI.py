# coding=utf-8

import locale
from flask import Flask 
from flask import render_template
from flask import request

app = Flask('285')
app = Flask(__name__.split('.')[0])

ts = ""
allotment = ""
fsp = ""
sc = ""
isp = ""
bc = ""
taxrate = ""

@app.route("/", methods=['GET', 'POST'])
def main():
	# return 'Hello, World!'
	result = 0
	error = ''
	if request.method=='POST':
		try:
			result = inputProfit().decode('utf8')
		except ValueError:
			error = 'Please input correct format information.'
	return render_template('index.html', result=result, error=error, ts = ts, allotment = allotment, fsp = fsp, sc = sc, isp = isp, bc = bc, taxrate = taxrate)


def printLocale(str):
	locale.setlocale(locale.LC_ALL, 'en_US')
	return locale.format("%.2f", str, grouping=True)

def costAndPrint(allotment, isp, fsp, sc, bc, taxrate):
	"This calculate the cost and print the cost details"
	taxrate = taxrate/100.0
	gain = allotment * (fsp - isp) - sc - bc
	cost = allotment * isp + sc + bc + gain * taxrate
	total = allotment * isp
	returnRate = gain*(1-taxrate)/cost;
	wrapper = """PROFIT REPORT:<br>
	Proceeds<br>
	$%s<br><br>
	Cost<br>
	$%s<br><br>
	Cost details: <br>
	Total Purchase Price<br>
	%d × $%d = %s<br>
	Buy Commission = %.2f<br>
	Sell Commission = %.2f<br>
	Tax on Capital Gain = %d %s of $%s = %s<br><br>
	Net Profit<br>
	$%s<br><br>
	Return on Investment<br>
	%.2f %s<br><br>
	To break even, you should have a final share price of<br>
	$%.2f"""
	whole = wrapper % (printLocale(allotment*fsp), printLocale(cost), allotment, isp, printLocale(total), bc, sc, taxrate*100, '%', printLocale(gain), printLocale(gain*taxrate), printLocale(gain*(1-taxrate)), returnRate*100, '%', (total+bc+sc)/100.0)
	return whole

def inputProfit():
	global ts
	ts = request.form['ticketS']
	global allotment 
	allotment = int(request.form['allotment'])
	checknum(allotment)
	global fsp
	fsp = float(request.form['fsp'])
	checknum(fsp)
	global sc
	sc = float(request.form['sc'])
	checknum(sc)
	global isp
	isp = float(request.form['isp'])
	checknum(isp)
	global bc
	bc = float(request.form['bc'])
	checknum(bc)
	global taxrate
	taxrate = float(request.form['taxrate'])
	checknum(taxrate)
	return costAndPrint(allotment, isp, fsp, sc, bc, taxrate)

def checknum(num):
	if num<0:
		raise ValueError

if __name__ == "__main__":
	app.run()