
import json

from django.shortcuts import render, get_object_or_404

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

#    try:
    decoded = json.loads(task.data)
    #print "JSON parsing example: ", decoded['properties']['taskDescription']['description']
    taskDescription = decoded['question']
    taskTitle = decoded['header']
    taskInput = decoded['input']
    additionalInput = decoded['additional_input']
    additional_header = decoded['additional_header']
    headers = decoded['headers']

    answers_amount = [i+1 for i in range(int(9))]
    #context = {'userid' : 'iwas', 'question': 'Meine Frage?', 'header' : 'Mein Header !', 'input' : 'Input is das ;-)', 'taskid' : '1', 'headers' : headers}
    context = {'userid' : 'MyUser', 'question' : taskDescription, 'header' : taskTitle, 'input' : taskInput, 'additional_input' : additionalInput, 'additional_header' : additional_header, 'taskid': task_id, 'headers' : headers, 'answers_amount' : answers_amount}
    return render(request, 'polls/task_temp.html', context)
  #  except (ValueError, KeyError, TypeError):
   #     print "JSON format error"

    return HttpResponse("Something went wrong with JSON")


def results(request, task_id):
    return HttpResponse("You're looking at the results of poll %s." % task_id)


def submit(request, task_id):
    if request.method == 'POST':  # If the form has been submitted...
    #print request.POST['keyword2']
        t = get_object_or_404(Task, id=task_id)

        try:
            decoded = json.loads(t.data)
            headers = decoded['headers']
            buff = "{'keywords': {"#'Windows': 'P', 'IBM': 'C', 'Microsoft': 'C'}}"
            
            for row in range(1,9):
	      buff += " , "
	      cnt = 0
	      for column in headers:
	        cnt = cnt+1;
		if cnt == len(headers):
		  buff += "'"+request.POST[column+'_'+str(row)]+"'"
		else:  
		  buff += "'"+request.POST[column+'_'+str(row)]+"' :"

	    buff += "}}"
	    #for column in headers:
            #    buff += column + ": \n"
            #    for row in range(0, 9):
            #        buff += "Row" + str(row) + ":  " + request.POST[column + '_' + str(row)] + "\n"


            # pretty printing of json-formatted string
            #  print json.dumps(decoded, sort_keys=True, indent=4)

            #  buff = request.POST['keyword1']+' ; '+request.POST['type1']+' ,\n '
            #  buff += request.POST['keyword2']+' ; '+request.POST['type2']+' ,\n '
            #  buff += request.POST['keyword3']+' ; '+request.POST['type3']+' ,\n '
            #  print buff
            t.answer = buff
            t.save()
            #print "JSON parsing example: ", decoded['title']
            #print "Complex JSON parsing example: ", decoded['two']['list'][1]['item']

        except (ValueError, KeyError, TypeError):
            print "JSON format error"

        return HttpResponse('Task finished successfully ')

    return HttpResponse('Somethng is wrong: Not POST Request Methode')

# Create your views here.
