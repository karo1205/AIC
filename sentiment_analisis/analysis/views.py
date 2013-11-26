from django.http import HttpResponse


from django.shortcuts import render, get_object_or_404

from analysis.models import Keyword, Sentiment

def query(request):
    
    context = {'userid' : 'MyUser', 'keywords' : Keyword.objects.all()}
    return render(request, 'analysis/query.html', context)

def result(request):
    
    sentiments = Sentiment.objects.filter(keyword = request.POST['selectbox'])	

    context = {'userid' : 'MyUser', 'sentiments' : sentiments, 'keyword' : Keyword.objects.get(id=request.POST['selectbox'])}
    return render(request, 'analysis/result.html', context)

# Create your views here.
