# -*- coding: utf-8 -*-
import time
from googlefinance import getQuotes
from yahoo_finance import Share
import json
import os
from pandas_datareader import data
from datetime import datetime, timedelta
# import itertools

def getStockPrice(string):
	data = None
	while data is None:
		try:
			dd = json.loads(readJsonStream(string))
			data=str(dd["LastTradePrice"])
		except Exception as e:
			print e.args
		try:
			stock = Share(string)
			data=str(stock.get_price())
		except Exception as e:
			print e.args
	return data
		

def readJsonFile():
	try:
		with open(os.getcwd()+'/investment-strategy/strategy-stock.json') as json_file_data:
			data=json.load(json_file_data)
	except Exception as e:
		with open(os.getcwd()+'/stock/investment-strategy/strategy-stock.json') as json_file_data:
			data=json.load(json_file_data)
	finally:
		return data

def readJsonStream(string):
	json_data = json.dumps(getQuotes(string), indent=2).replace("[", "").replace("]", "")
	# print(json_data)
	return json_data

def getSelectedStocks(selectedStrategy):
	sStr = readJsonFile()[selectedStrategy]
	# print sStr
	sStock = []
	portion = []
	for stock in sStr:
		sStock.append(stock['name'])
		portion.append(stock['portion'])
	dictd = {}
	dictd['name'] = sStock
	dictd['portion'] = portion
	# print dictd
	return dictd

def bought1(money, selectedStrategy):
	dictStock = getSelectedStocks(selectedStrategy)
	shares = []
	pricel = []
	# print dictStock['name'][0]
	for i in range(0,len(dictStock['name'])):
		n = str(dictStock['name'][i])
		p = int(dictStock['portion'][i])
		print n, p
		# rjs = readJsonStream(n)
		# print rjs
		pp = str(getStockPrice(n))
		# print pp
		price = float(pp)
		monportion = money * p / 100
		share = int(monportion / price)
		shares.append(share)
		pricel.append(price)
	dictStock['shares'] = shares
	dictStock['price'] = pricel
	return dictStock

def bought2(money, selectedStrategy1, selectedStrategy2):
	dictStock1 = getSelectedStocks(selectedStrategy1)
	dictStock2 = getSelectedStocks(selectedStrategy2)
	shares1 = []
	shares2 = []
	pricel1 = []
	pricel2 = []
	# print dictStock['name'][0]
	for i in range(0,len(dictStock1['name'])):
		# print i
		n = str(dictStock1['name'][i])
		p = int(dictStock1['portion'][i])
		# print n, p
		# rjs = readJsonStream(n)
		# print rjs
		pp = str(getStockPrice(n))
		# print pp
		price = float(pp)
		monportion = money / 2 * p / 100
		share = int(monportion / price)
		shares1.append(share)
		pricel1.append(price)
	dictStock1['shares'] = shares1
	dictStock1['price'] = pricel1

	for i in range(0,len(dictStock2['name'])):
		n = str(dictStock2['name'][i])
		p = int(dictStock2['portion'][i])
		# print n, p
		# rjs = readJsonStream(n)
		# print rjs
		price = float(str(getStockPrice(n)))
		monportion = money / 2 * p / 100
		share = int(monportion / price)
		shares2.append(share)
		pricel2.append(price)
	dictStock2['shares'] = shares2
	dictStock2['price'] = pricel2
	dictStock1['name'] = dictStock1['name']+dictStock2['name']
	dictStock1['portion'] = dictStock1['portion']+dictStock2['portion']
	dictStock1['shares'] = dictStock1['shares']+dictStock2['shares']
	dictStock1['price'] = dictStock1['price']+dictStock2['price']
	# print dictStock1;
	return dictStock1;

def sumVal(dictS):
	sum = 0
	dictStock = dictS
	for i in range(0,len(dictStock['name'])):
		shares = int(dictStock['shares'][i])
		name = str(dictStock['name'][i])
		price = float(str(getStockPrice(name)))
		sum += (price * shares)
	return sum

def diffVal(money, dictS):
	return money - sumVal(dictS)

def getHistoryData(dictS):
	sum=0
	dictHistory={}
	for x in dictS['name']:
		name = str(x)
		num = hisdf[name]
		print num
		for i in range(0,len(num)):
			dat = str(num['Date'][i])
			dictHistory[dat]=0
	for x in dictS['name']:
		num = hisdf[str(x)]
		name = ''
		for i in range(0,len(num)):
			if name is not str(x):
				dat = str(num['Date'][i])
				sum = dictHistory[dat]
				shares = int(dictS['shares'][dictS['name'].index(str(x))])
				price = float(num['Close'][i])
				dat = str(num['Date'][i])
				sum += (price * shares)
				dictHistory[dat] = sum
				name = str(x)
	return dictHistory
	
def isWeekDay(date):
	day = date.isoweekday()
	# print day
	return day < 6 and day > 0

def SevenDaysBefore(date):
	return date - timedelta(days=7)

def refreshData():
	global hisdf
	hisdf = {}
	for i in range(0,len(readJsonFile()["Investment Strategies"])):
		file = getSelectedStocks(str(readJsonFile()["Investment Strategies"][i]))
		for x in file['name']:
			day = datetime.today()
			num = data.DataReader(str(x),'google',SevenDaysBefore(day),day)[-5:]
			num.reset_index(inplace=True,drop=False)
			hisdf[str(x)] = num;
refreshData()
# print hisdf
# print getHistoryData(bought1(5000, "Growth Investing"))
# print getStockPrice("BIIN")
# print readJsonStream("VTI")
# print bought1(5000, "Growth Investing")
# print bought2(15000, "Index Investing", "Ethical Investing")
# dictS = bought2(15000, "Index Investing", "Ethical Investing")
# print sumVal(dictS)
# print diffVal(15000, dictS)
# print isWeekDay(datetime.today())
# print getHistoryData(bought1(5000, "Index Investing"))