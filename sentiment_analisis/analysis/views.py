from django.http import HttpResponse


from django.shortcuts import render, get_object_or_404

from analysis.models import Keyword, Sentiment, Order

def query(request):
    
    context = {'userid' : 'MyUser', 'keywords' : Keyword.objects.all()}
    return render(request, 'analysis/query.html', context)

def confirm(request):
#TODO:    order = Order(keyword)
    
    
    keywords = request.POST.getlist('mytextarea')
    budget = request.POST['budget']
    datestart = request.POST['datestart']
    dateend = request.POST['dateend']
    userid = request.POST['username']
    #order = Order()

    context = {'userid' : 'USERNAME', 'keywords' : {'WORD1','WORD2'}, 'startdate' : 'STARTDATE', 'enddate' : 'ENDDATE', 'budget' : 'BUDGET' }
    return render(request, 'analysis/confirm.html',context)

def result(request):
    
#    sentiments = Sentiment.objects.filter(keyword = request.POST['selectbox'])	

    context = {'userid' : 'MyUser', 'sentiments' : {1,2}, 'keyword' : 'keyword1'}#Keyword.objects.get(id=request.POST['selectbox'])}
    return render(request, 'analysis/result.html', context)

# Create your views here.
