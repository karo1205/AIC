from django.http import HttpResponse

import datetime

from django.shortcuts import render, get_object_or_404

from analysis.models import Keyword, Sentiment, Order, Feed, Task

def query(request):
    
    context = {'userid' : 'MyUser', 'keywords' : Keyword.objects.all()}
    return render(request, 'analysis/query.html', context)

def confirm(request):

    if not request.method == 'POST':    
      print "Not Post !"
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
    

#    username = request.POST.get('username')
    order = Order(budgetlimit = budget, start_date = datestart, end_date = dateend, customer = username) 
    
    order.save()
    for k in keys:
      order.keyword.add(k)
    order.save()
    
# get all feeds from relevant time # TODO: Task or Feed Date ? 
#    print keys
#    allkeywords = Keyword.objects.filter(self__in = keys)
    
    allfeeds = []
    for tmpkey in keys:
      for tmp in tmpkey.feed.exclude(pub_date__gte=dateend).filter(pub_date__gte=datestart):
        allfeeds.append(tmp)
    
    
    print allfeeds

    task_amount = int((int(budget)/10) * 3) 
   
    for i in range(0, task_amount):
      for feed in allfeeds:
        print "create Task2 with "+str(feed)    
   

#TODO: Create Task2 s 

 
       
#    if not alltasks:
#      print "no feed for this keywords"
 #     return render(request,'analysis/error.html')
    #allfeeds = Feed.objects.filter(id__in= alltask)
#    allfeeds = []
#    for buftask in alltasks:
#      allfeeds.append(buftask.feed)
    

#    print allfeeds   
    
#    task_amount = budget * 

    context = {'userid' : username, 'keywords' : keywords, 'startdate' : datestart, 'enddate' : dateend, 'budget' : budget }
    return render(request, 'analysis/confirm.html',context)

def error(request):
  context = {'userid' : 'user'}
  return render(request, 'analysis/error.html',context) 

def result(request):
    
#    sentiments = Sentiment.objects.filter(keyword = request.POST['selectbox'])	

    context = {'userid' : 'MyUser', 'sentiments' : {1,2}, 'keyword' : 'keyword1'}#Keyword.objects.get(id=request.POST['selectbox'])}
    return render(request, 'analysis/result.html', context)

# Create your views here.
