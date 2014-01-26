import json
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, loader
from polls.models import Task, Worker


def index(request):
#    latest_poll_list = Task.objects.all().order_by('-id')[:5]
#    context = {'latest_poll_list': latest_poll_list}
    test  = 'Meine UserId'
    test2 = 'Das ist noch ein Test :-)'
    headers = {'Header1', 'Header2', 'Header3'}
    context = {'userid' : test, 'question': 'Meine Frage?', 'header' : 'Mein Header !', 'input' : 'Input is das ;-)', 'taskid' : '1', 'headers' : headers}
    return render(request, 'polls/task_temp.html', context)

def detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
#<<<<<<< HEAD


#    try:
#      decoded = json.loads(task.data)
    #  headers = {'Header1', 'Header2', 'Header3'}
#      print "JSON parsing example: ", decoded['properties']['taskDescription']['description']
#      taskDescription = decoded['properties']['taskDescription']['description']
#      taskTitle = decoded['properties']['taskTitle']['description']
#      taskInput = decoded['properties']['input']['description']
#      additionalInput = decoded['properties']['additionalInput']['description']
#      additional_header = decoded['properties']['additionalInputHeader']['description']
#      headers = decoded['properties']['resultColumns']['description']
#
#      answers_amount = decoded['properties']['countOfAnswers']['description']
#
#      answers_amount = [i+1 for i in range(int(answers_amount))]
#
#      #context = {'userid' : 'iwas', 'question': 'Meine Frage?', 'header' : 'Mein Header !', 'input' : 'Input is das ;-)', 'taskid' : '1', 'headers' : headers}
#      context = {'userid' : 'MyUser', 'question' : taskDescription, 'header' : taskTitle, 'input' : taskInput, 'additional_input' : additionalInput, 'additional_header' : additional_header, 'taskid': task_id, 'headers' : headers, 'answers_amount' : answers_amount}
#
#
#      return render(request, 'polls/task_temp.html', context)
#    except (ValueError, KeyError, TypeError):
#      print "JSON format error"
#=======

    try:
      decoded = json.loads(task.data)
    #print "JSON parsing example: ", decoded['properties']['taskDescription']['description']
      taskDescription = decoded['question']
      taskTitle = decoded['header']
      taskInput = decoded['input']
      additionalInput = decoded['additional_input']
      additional_header = decoded['additional_header']
      headers = decoded['headers']

      answers_amount = [i + 1 for i in range(int(9))]
    #context = {'userid' : 'iwas', 'question': 'Meine Frage?', 'header' : 'Mein Header !', 'input' : 'Input is das ;-)', 'taskid' : '1', 'headers' : headers}
      context = {'userid' : 'MyUser', 'question' : taskDescription, 'header' : taskTitle, 'input' : taskInput, 'additional_input' : additionalInput, 'additional_header' : additional_header, 'taskid': task_id, 'headers' : headers, 'answers_amount' : answers_amount}
    #return render(request, 'polls/task_temp.html', context)
      return render_to_response('polls/task_temp.html', RequestContext(request, context))
    except (ValueError, KeyError, TypeError):
        print "JSON formaterror"

    return HttpResponse("Something went wrong with JSON")


def results(request, task_id):
    return HttpResponse("You're looking at the results of poll %s." % task_id)


def submit(request, task_id):
    if request.method == 'POST':  # If the form has been submitted...
        t = get_object_or_404(Task, id=task_id)
	print request
        try:
            decoded = json.loads(t.data)
            headers = decoded['headers']
            try:  # see if worker alread is known
              w = Worker.objects.get(name=request.POST.get("worker"))
            except Worker.DoesNotExist:
                    # create new worker
              newworker=Worker(name=request.POST.get("worker"))
              newworker.save() # save befor assigning to t becasue newworker hast'got an id yet
              t.worker_id=newworker.id
              t.save()

	    buff={}
            buff['worker']=request.POST.get("worker")
            buff['keywords']={}
	    
            for row in range(1,9):
             # print request.POST[headers[0] + '_' + str(row)]+" : "+ request.POST[headers[1] + '_' + str(row)]      
	      buff['keywords'][request.POST[headers[0] + '_' + str(row)]]=request.POST[headers[1] + '_' + str(row)]
            t.answer = buff
            t.save()

        except (ValueError, KeyError, TypeError):
            print "JSON format error"

        return HttpResponse('Task finished successfully ')

    return HttpResponse('Somethng is wrong: Not POST Request Methode')

