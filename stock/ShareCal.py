# coding=utf-8

import locale

def printLocale(str):
	locale.setlocale(locale.LC_ALL, 'en_US')
	return locale.format("%.2f", str, grouping=True)

def checkInputInt(data):
	while True:
		try:
			data = int(data)
		except Exception as e:
			data = raw_input("Please enter a valid integer:")
			continue
		else:
			break
	return data

def checkInputFloat(data):
	while True:
		try:
			data = float(data)
		except Exception as e:
			data = raw_input("Please enter a valid float:")
			continue
		else:
			break
	return data

def costAndPrint(allotment, isp, fsp, sc, bc, taxrate = 0.15):
	"This calculate the cost and print the cost details"
	gain = allotment * (fsp - isp) - sc - bc
	cost = allotment * isp + sc + bc + gain * taxrate
	total = allotment * isp
	returnRate = gain*(1-taxrate)/cost;
	print "PROFIT REPORT:"
	print "Proceeds"
	print "$%s"% (printLocale(allotment*fsp))
	print "\nCost"
	print "$%s"% (printLocale(cost))
	print "\nCost details: "
	print "Total Purchase Price"
	print "%d × $%d = %s" % (allotment, isp, printLocale(total))
	print "Buy Commission = %.2f" % (bc)
	print "Sell Commission = %.2f" % (sc)
	print "Tax on Capital Gain = "+str(int(taxrate*100))+"%"+" of $"+printLocale(gain)+" = "+printLocale(gain*taxrate)
	print "\nNet Profit"
	print "$%s"% (printLocale(gain*(1-taxrate)))
	print "\nReturn on Investment"
	str_rate = "%.2f" % (returnRate*100)
	print str_rate+"%"
	print "\nTo break even, you should have a final share price of"
	print "$%.2f" % ((total+bc+sc)/100.0)

def inputProfit():
	print "Compute Your Profit:"
	ticketS = raw_input("\nTicker Symbol: \n")
	allotment = checkInputInt(raw_input("\nAllotment: \n"))
	fsp = checkInputFloat(raw_input("\nFinal Share Price: \n"))
	sc = checkInputFloat(raw_input("\nSell Commission: \n"))
	isp = checkInputFloat(raw_input("\nInitial Share Price: \n"))
	bc = checkInputFloat(raw_input("\nBuy Commission: \n"))
	taxrate = checkInputFloat(raw_input("\nCapital Gain Tax Rate (%): \n"))/100.0
	print ""
	costAndPrint(allotment, isp, fsp, sc, bc, taxrate)

inputProfit()