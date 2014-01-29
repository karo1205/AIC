from django.http import HttpResponse

import datetime

from django.shortcuts import render, get_object_or_404

from analysis.models import Keyword, Sentiment, Order, Feed, Task

from analysis.utils import *

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def query(request):
    
    context = {'userid' : 'MyUser', 'keywords' : Keyword.objects.all()}
    return render(request, 'analysis/query.html', context)

def confirm(request):

    if not request.method == 'POST':    
      logger.error("Confirm: Not Post !")
      http.HttpResponseForbidden()
  
    keywords = request.POST.getlist('mytextarea[]')

    username = request.POST.get('username')
 
   
    keys = []
    for ids in keywords:
      keys.append(get_object_or_404(Keyword, id=ids))
   
# create new Order and save it to db
    try: 
      budget = request.POST.get('budget')
      int(budget)
    except ValueError:
      context = {'userid' : username, 'error_message' : 'Error! Budget has to be a number !'}
      return render(request, 'analysis/error.html',context)
    
    try:
      datestart = request.POST.get('datestart')
      dateend = request.POST.get('dateend')
      datetime.datetime.strptime(datestart, '%Y-%m-%d')
      datetime.datetime.strptime(dateend, '%Y-%m-%d')
    except ValueError:
      context = {'userid' : username, 'error_message' : 'Error! Dates has to be written as YYYY-MM-DD !'}
      return render(request, 'analysis/error.html',context)
    
    order = Order(budgetlimit = budget, start_date = datestart, end_date = dateend, customer = username) 
    
    order.save()
    for k in keys:
      order.keyword.add(k)
    order.save()
    
# get all feeds from relevant time 
    totallength = 0
    counter = 0
    allfeeds = []
    for tmpkey in keys:
      for tmp in tmpkey.feed.exclude(pub_date__gte=dateend).filter(pub_date__gte=datestart):
        allfeeds.append(tmp)
        totallength += tmp.content.__len__()
        counter = counter + 1

# calculate task amount and create Task2 s 
    if counter > 0:       
      task_amount = int(((int(budget))/((totallength/counter)+1))/10) 
      min_amount = int((((totallength/counter)+1)*10))
    else:
      task_amount = 1
      min_amount = 5

    if task_amount < 1:
      context = {'userid' : username, 'error_message' : 'Error! Too less budget, you need at least '+str(min_amount)+' or choose less keywords!'}
      return render(request, 'analysis/error.html',context)
 
#    logger.info('!!range(0,'+str(task_amount))
#    logger.info("!! all Feeds are: "+str(allfeeds)) 
    if len(allfeeds) < 1:
      context = {'userid' : username, 'error_message' : 'Error! No Articles found at the given timeperiod: '+str(datestart)+' - '+str(dateend)+' !'}
      return render(request, 'analysis/error.html',context)
   
    logger.info(task_amount)
    for i in range(0, task_amount):
      for feed in allfeeds:
#        logger.info('!!bin in schleife')        
        post_task2_to_crowd(feed,int(int(budget)/(task_amount+1)))
	logger.info("create Task2 with "+str(feed)+"and price "+str(int(budget)/(task_amount+1)))    

#Create Task2s 

    context = {'userid' : username, 'keywords' : keywords, 'startdate' : datestart, 'enddate' : dateend, 'budget' : budget }
    return render(request, 'analysis/confirm.html',context)

def error(request):
  context = {'userid' : 'user'}
  return render(request, 'analysis/error.html',context) 

def result(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    keywords = order.keyword.all() 

    allsentiments =  Sentiment.objects.all()

    sentiments = []
    sumkeys = {}
    countkeys = {} 
    for s in allsentiments:
      for k in keywords:
        if s.keyword == k:
          sentiments.append(s)
	  try:
            sumkeys[k] = sumkeys[k]+s.score
          except KeyError:
            sumkeys[k] = s.score
          try:       
            countkeys[k] = countkeys[k] + 1
          except KeyError:
            countkeys[k] = 1

    sentiments = sorted(sentiments, key=lambda sentiment: sentiment.com_date)
 
    logger.info('Sorted Sentiments for result: '+str(sentiments))
    
    averagekeys = {}
    allkeystext = []
    for keys in sumkeys.keys():
       allkeystext.append(keys.text)
       averagekeys[keys] = sumkeys[keys] / countkeys[keys]  
    
    #print averagekeys.values()
    #print sentiments
    
    keylist = {}
    stringlist = ""
    for s in sentiments:
      try:
        keylist[s.keyword].append(s.score)
    #    print keylist[s.keyword]
      except KeyError:
        keylist[s.keyword] = [s.score]
  
    stringlist =  str(keylist.values())
    #print "MYSTRIN: "+ stringlist
    stringlist = stringlist.replace('], [','|')
    stringlist = stringlist.replace('[','')
    stringlist = stringlist.replace(']','')   
    #print "MYSTRIN: "+ stringlist


    context = {'userid' : 'MyUser', 'sentiments' : sentiments,'averages' : averagekeys, 'allkeys' : allkeystext, 'allvaluesavg' : averagekeys.values(), 'allvalues' : stringlist }
    return render(request, 'analysis/result.html', context)

# Create your views here.
