from django.http import HttpResponse


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
    
    keys = []
    for ids in keywords:
      keys.append(get_object_or_404(Keyword, id=ids))
   
# create new Order and save it to db
    budget = request.POST.get('budget')
    datestart = request.POST.get('datestart')
    dateend = request.POST.get('dateend')
    username = request.POST.get('username')
    order = Order(budgetlimit = budget, start_date = datestart, end_date = dateend, customer = username) 
    order.save()
    for k in keys:
      order.keyword.add(k)
    order.save()
    
# get all feeds from relevant time # TODO: Task or Feed Date ? 
    print keys
#    allkeywords = Keyword.objects.filter(self__in = keys)
    
    allfeeds = []
    for tmpkey in keys:
      allfeeds.append(tmpkey.feed.exclude(pub_date__gte=dateend).filter(pub_date__gte=datestart))
    
 
    print allfeeds
     
       
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

def result(request):
    
#    sentiments = Sentiment.objects.filter(keyword = request.POST['selectbox'])	

    context = {'userid' : 'MyUser', 'sentiments' : {1,2}, 'keyword' : 'keyword1'}#Keyword.objects.get(id=request.POST['selectbox'])}
    return render(request, 'analysis/result.html', context)

# Create your views here.
