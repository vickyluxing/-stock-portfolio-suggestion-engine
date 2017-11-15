#coding = utf8
from datetime import datetime
import tzlocal
from yahoo_finance import Share

def getPDT():
	now = datetime.now(tzlocal.get_localzone())
	line = now.ctime()
	timezone = now.tzname()
	year = now.year
	index = line.find(str(year))
	return line[:index]+timezone+" "+line[index:]

def getSymbol():
	return raw_input("Please enter a symbol: \n").upper()

def getFullName(str):
	return Share(str).get_name()+" ("+str+")"

def getPriceNChange(str):
	stock = Share(str)
	return stock.get_price()+' '+stock.get_change()+' ('+stock.get_percent_change()+')'

def checkSymbol(str):
	if str=='exit'.upper():
		return
	while not Share(str).get_name():
		print "Not a stock"
		str = getSymbol()
	return str

# while True:
# 	try:
# 		sym = getSymbol()
# 		if sym=='exit'.upper():
# 			break
# 		sym = checkSymbol(sym)
# 		print ""
# 		print getPDT()
# 		print getFullName(sym)
# 		print getPriceNChange(sym)
# 		print ""
# 	except Exception as e:
# 		print e
		
	
