from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from django.template import loader
# from task import process_strategy, gettoday_price, check_db, draw_portfoliochart, draw_piechart
from stockCal import *
# Create your views here.

import string

def test():
    return HttpResponse("Hello, world")



portfolio_strategies = readJsonFile()["Investment Strategies"]
# print len(portfolio_strategies)
# portfolio_keys = []

def choices(portfolio_strategies):
    strategies_choices = ()
    for s in range(0, len(portfolio_strategies)):
        strategies_choices += ((str(portfolio_strategies[s]), str(portfolio_strategies[s])),)
    return strategies_choices

global Schoices, hisDict
hisDict = {}
Schoices = choices(portfolio_strategies)

# print Schoices

# for strategy in portfolio_strategies:
#     portfolio_keys.append(strategy.split(' ')[0].lower())
# for strategy in zip(portfolio_strategies, portfolio_keys):
#     strategies_choices += ((strategy[1], strategy[0]),)

class selectionform(forms.Form):
    strategies = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True, choices=Schoices, help_text='Please select investment strategy')
    # strategies = forms.ChoiceField(required=True, choices=Portfolio_strategies)
    allotment = forms.DecimalField(required=True, help_text='Total amount to be invested(minimum $5000 USD)',min_value=5000)

    # def clean(self):
    #     data = self.cleaned_data['strategies']
    #     if len(data) > 2:
    #         raise forms.ValidationError("Please only choose one or two strategies!")


def portfolio(request):
    form = selectionform()
    global stocklist
    global allotment
    global dic
    if request.POST:
        try:
            dic={}
            selectDict={}
            priceDict={}
            shareDict = {}
            form = selectionform(request.POST)
            if form.is_valid():
                params = request.POST.copy()
                allotment = float(params['allotment'])
                choice = params.getlist('strategies')
                print allotment, choice, 'in side the POST'
                #choice represents the investment strategies selected
                
                if len(choice)==1:
                    dic = bought1(allotment, str(choice[0]))
                    stocklist = dic['name']
                    for x in range(0,len(stocklist)):
                        selectDict[str(stocklist[x])]=int(dic['portion'][x])
                        shareDict[str(stocklist[x])]=int(dic['shares'][x])
                        priceDict[str(stocklist[x])]=float(dic['price'][x])
                    print selectDict
                    print stocklist
                elif len(choice)==2:
                    dic=bought2(allotment, str(choice[0]), str(choice[1]))
                    stocklist = dic['name']
                    for x in range(0,len(stocklist)):
                        selectDict[str(stocklist[x])]=int(dic['portion'][x])
                        shareDict[str(stocklist[x])]=int(dic['shares'][x])
                        priceDict[str(stocklist[x])]=float(dic['price'][x])
                    print stocklist
                    print selectDict
                else:
                    raise forms.ValidationError("Please only choose one or two strategies!")

            script = ''
            div = ''
            tablehtml = ''
            piescript = ''
            piediv = ''

            his = getHistoryData(dic)
            print his
            current = sumVal(dic)+diffVal(allotment,dic)


            return render(request, 'result.html',
                                  {'the_script': script, 'the_div': div, 'stocktable': tablehtml,
                                   'pie_script': piescript, 'pie_div': piediv, 'stocks': stocklist, 
                                   'amount': allotment, 'his': his, 'selectDict': selectDict,
                                   'share': shareDict, 'price': priceDict, 'current':current
                                   })
        except Exception, e:
            print e.args
            return render(request,'error.html')


    return render(request,'index.html', {'form':form})


def refresh(request):
    # msg = check_db()
    form = selectionform()
    refresh()
    return render(request, 'index.html', {'form':form})

def currentval(request):
    current = sumVal(dic)+diffVal(allotment,dic)
    return render(request, 'currentval.html', {'current':current})
