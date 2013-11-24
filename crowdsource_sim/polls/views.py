
import json

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.http import Http404

from django.template import RequestContext, loader

from polls.models import Task, Worker


def index(request):
    latest_poll_list = Task.objects.all().order_by('-id')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'polls/detail.html', {'task': task})

def results(request, task_id):
    return HttpResponse("You're looking at the results of poll %s." % task_id)

def submit(request, task_id):
    if request.method == 'POST': # If the form has been submitted...
      #print request.POST['keyword2']
      
      t = get_object_or_404(Task, id=task_id)
      try:
        decoded = json.loads(t.data)
 		
       # pretty printing of json-formatted string
        print json.dumps(decoded, sort_keys=True, indent=4)
 
        buff = request.POST['keyword1']+' ; '+request.POST['type1']+' ,\n '
        buff += request.POST['keyword2']+' ; '+request.POST['type2']+' ,\n '
        buff += request.POST['keyword3']+' ; '+request.POST['type3']+' ,\n '
        print buff
        t.answer = buff
	t.save()
	#print "JSON parsing example: ", decoded['title']
        #print "Complex JSON parsing example: ", decoded['two']['list'][1]['item']
 	
      except (ValueError, KeyError, TypeError):
        print "JSON format error"

      return HttpResponse('Ausgabe: ')
       

    return HttpResponse('Somethng is wrong: Not POST Request Methode') 

# Create your views here.
