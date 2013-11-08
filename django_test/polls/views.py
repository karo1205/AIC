# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from polls.models import Poll
from django.http import Http404
from django.shortcuts import render


def index(request):
    """Docstring."""

    latest_question_list = Poll.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = RequestContext(request, {
                'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))


def detail(request, question_id):
    """Docstring."""
    try:
        question = Poll.objects.get(pk=question_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, "polls/details.html", {'question': question})


def results(request, question_id):
    """Docstring."""

    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    """Docstring."""

    return HttpResponse("You're voting on question %s." % question_id)
