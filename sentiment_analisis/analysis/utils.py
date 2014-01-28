""" This module contains helper functions needed for preccessing data coming from
the crowdsorucing platform
"""
import json
import urllib2
import requests
import nltk
import random
import logging
from analysis.models import Task, Keyword, Sentiment, Feed
from analysis.models import Task, Keyword, Sentiment, Feed, Worker
from django.utils import timezone

logger = logging.getLogger(__name__)


def transform_task_to_data(task):

    """This function generates a JSON Structure out of the properties of the
    specific task

    """

    if task.question=="Question1":
        data={}
        data['header'] = "Identify Product and Company Names"
        data['question'] = """
        Please read this text carefully, filter out product and
        company names and put them into the textfields below.
        """
        data['additional_header'] = "Instructions"
        data['additional_input'] = "Please identifiy product and company names out of the given text and put the names into the 'keywords' collumn. Further put either a 'C' for company or a 'P' for product in to the second collumn"
        data['headers'] = [{"text":"Keyword","values":[],"type":"input"}, {"text":"[P]roduct or [C]ompany?","values":["P","C"],"type":"combo"}]
        data['input'] = nltk.clean_html(task.feed.content)
        data['keyword_count'] = 5
    elif task.question == "Question2":
        data = {}
        data['header'] = "Sentiment regarding Product and Company Names"
        data['question'] = """
        Please read this text carefully and rate your sentiment regarding the keywords provided below.
        Please rate how positive do you think the keyword is mentioned in the text.
        1......very positive
        2......positive
        3......neutral
        4......negative
        5......very negative
        """
        data['additional_header'] = ""
        data['additional_input'] = []
        for kw in task.feed.keyword_set.values():
            data['additional_input'].append(kw['text'])

        data['headers'] = [{"text":"Keyword","values":[],"type":"input_readonly"}, {"text":"Your Sentiment?","values":["1","2","3","4","5"],"type":"combo"}]
        data['input'] = nltk.clean_html(task.feed.content)
        data['keyword_count'] = len(data['additional_input'])
    else:
        logger.error("Format Error: Please check content of task " + str(task.id))
    return data


def post_task2_to_crowd(f):
    """
        This function post a task to the
        crowd.
    """

    t = Task(pub_date=timezone.now(), question='Question2', feed=f)
    t.save()
    logger.info("new task2 was stored")
    payload = json.load(urllib2.urlopen('http://127.0.0.1:8002/api/v1/task/1/?format=json'))
    payload['data'] = json.dumps(transform_task_to_data(t))
    payload['price'] = 0
    payload['question'] = 'Please state your sentiments about this text'
    #TODO: callback uri
    payload['callback_uri'] = 'http://127.0.0.1:8000/api/v1/task/'+ str(t.id) +'/'
    #payload['keyword_count'] = 5
    payload.pop('resource_uri')
    payload.pop('id')
    logger.info('payload = ' + json.dumps(payload)[:50])
    url = 'http://127.0.0.1:8002/api/v1/task/'

    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201:
        logger.info("Task sucessfull postet: " + str(response.status_code) + " " + response.reason)
        t.status = 'S'
        t.task_uri = response.headers.get('location')  # get the location of the saved Item
        t.save()
    else:
        logger.error("Problem with CrowdSourcing App: " + str(response.status_code) + " " + response.reason)


def process_task_answers():

    """
    This funcion  goes trough all unprocessed tasks and add news
    keywords,sentiments, workes and relations

    """

    logger.info("start processing... ")


    opentasks = Task.objects.filter(status='D')  # get all started tasks
    logger.info('Getting done tasks from DB. ' + str(opentasks.count()) + ' elements found')
    for t in opentasks:
        logger.info("Processing Task " + str(t.id))
        try:
            answer = json.loads(t.answer)
            #answer = t.answer
        except ValueError:
            logger.error("the answer field of task " + str(t.id) + " does not contain a valid JSON Format. Skipping.")
            continue    # if there is not valid JSON there is no pint of considerung this answer
                        # TODO: Implement quality control and pot task
                        # again

        # Process Task Type 1
        if t.question == "Question1":
            logger.info("processing question1... ")
            for kw in answer['keywords'].keys():
                try:
                    keyword = Keyword.objects.get(text = kw, category = answer['keywords'][kw])
                    logger.info('Keyword "' + kw + '" already in DB')
                    t.keywords.add(keyword)  # add Task --> Keyword Relationship
                    keyword.feed.add(t.feed)  # add Keyword --> Feed Relationship
                    keyword.save()
                    logger.info('Keyword "' + kw + '" assigned to Task' + str(t.id))
                    keyword_inverse = Keyword.objects.filter(text=kw).exclude(category=answer['keywords'][kw])
                    if len(keyword_inverse) == 0:
                        logger.info("no inverse keyword found. skipping")
                        continue
                    elif keyword.task_set.count() / (keyword_inverse[0].task_set.count() + keyword.task_set.count()) <= 0.34:
                        t.worker.score -= 1
                        t.worker.save()
                        logger.info('Keyword "' + kw + '" has wrong catgory set.' + str(t.worker.id)+ ' was degraded')
                    else:
                        logger.info("no penalty with" + str(keyword.task_set.count() / (keyword_inverse[0].task_set.count() + keyword.task_set.coun())))
                except Keyword.DoesNotExist:
                    if t.feed.content.find(kw) == -1:  #if keyword is not found in text of the feed
                        t.worker.score -= 1
                        t.worker.save()
                        logger.info('Keyword "' + kw + '" was not found in feed. worker ' + str(t.worker.id)+ ' was degraded')
                    else:   # TODO: Debug here
                        newkeyword=Keyword(text=str(kw), category=answer['keywords'][kw])
                        newkeyword.save()
                        t.keywords.add(newkeyword)
                        newkeyword.feed.add(t.feed)  # add Keyword --> Feed Relationship
                        newkeyword.save()
                        logger.info('new keyword "' + kw + '" created and assigned to Task' + str(t.id))
            #uncomment the following line if no autmatic post of task 2 is required
            post_task2_to_crowd(t.feed)

        # Process Task Type 2
        elif t.question == "Question2":
            logger.info("processing question1... ")
            for sen in answer['keywords'].keys():
                logger.info("processing Sentiment " + sen + "(" + answer['keywords'][sen] + ")")
                keywords = Keyword.objects.filter(text=sen)
                if len(keywords) == 0:
                    logger.error("Received sentiment for non existing Keyword")
                    continue
                else:
                    # Quality Contol
                    new_score = answer['keywords'][sen]
                    scores=[]
                    for k in keywords:
                        scores.extend(k.get_sentiment_scores())
                        print scores
                    if len(scores) <= 3:
                        logger.info("to few sentiments: Keyword " + sen + "has only " + str(len(scores)) + " sentiments")
                    elif abs(median(scores) - int(new_score)) >= 3:
                        logger.info("bad sentiment")
                        t.worker.score -= 1
                        logger.info('Worker ' + str(t.worker.id)+ ' was degraded')
                    #save sentiment
                    new_sentiment = Sentiment(score=new_score)
                    new_sentiment.worker = t.worker  # all the are Forein Keys of Sentiment
                    new_sentiment.feed = t.feed
                    new_sentiment.keyword = keywords[0] # choose better keyword instead of always thealways the  first
                    new_sentiment.save()
                    logger.info('new sentiment "' + sen +
                                '" created with score "' + str(new_sentiment.score) +
                                '" and relationships set: worker=' + t.worker.worker_uri +
                                ' feed=' + str(t.feed.id) +
                                ' keyword=' + str(keywords[0].text))
        else:
            logger.error("Keywords/Sentiments could not be processed.Something is wrong with task")

        t.status = 'P'  # set status to processed
        t.save()


def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    print mylist
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]


def create_test_sentiment_data(count):
    t = Task(question="Question2",
             feed_id=0)
    t.answer = {}
    t.answer['worker'] = 'testworker'
    t.answer['keywords'] = {}
    t.status = 'D'
    t.feed = Feed.objects.order_by('?')[0]
    for i in range(0,count):
        rand_keyword = Keyword.objects.order_by('?')[0]
        rand_sen = random.randint(1,5)
        t.answer['keywords'][rand_keyword.text]=str(rand_sen)
        print "rand sentiment" + str(rand_sen) + " for keyword " + rand_keyword.text
    print t.answer
    t.answer=json.dumps(t.answer)
    t.save()


def populate_db(min_sentiment = 10, min_worker = 1, min_feeds = 1, min_keywords = 1):
  logger.info('Start populating database...')
  all_worker = Worker.objects.all()
  if all_worker.__len__() < min_worker:
    for i in range(0,min_worker-len(all_worker)):
      Worker(score = 10, blocked = False).save()  

  all_worker = Worker.objects.all()
  
  logger.info('All Worker are: '+str(all_worker))  

  all_feeds = Feed.objects.all()
  if all_feeds.__len__() < min_feeds:
    for i in range(len(all_feeds),min_feeds):
      Feed(title = 'myTitle'+str(i), link = 'myLink'+str(i), content = 'myContent'+str(i), pub_date = timezone.now()).save()
  
  all_feeds = Feed.objects.all()

  logger.info('All Feeds are: '+str(all_feeds))

  all_keywords = Keyword.objects.all()
  if all_keywords.__len__() < min_keywords:
    new_keywords = []
    for i in range(0,min_keywords-len(all_keywords)):
      new_keywords.append(Keyword(text='keyword'+str(i),category='C',score = 10))
      new_keywords[i].save()
      new_keywords[i].feed = all_feeds[0:random.randint(0,len(all_feeds)-1)]
      new_keywords[i].worker = all_worker[0:random.randint(0,len(all_worker)-1)]
      new_keywords[i].save()
  
  
  all_keywords = Keyword.objects.all()
  
  logger.info('All Keywords are: '+str(all_keywords))

  all_sentiments = Sentiment.objects.all()
  
  if len(all_sentiments) < min_sentiment:
    new_sents = []
    for i in range(0,min_sentiment-len(all_sentiments)):
      new_sents.append(Sentiment(score=random.randint(0,5),com_date = timezone.now(),worker = all_worker[random.randint(0,len(all_worker)-1)],feed = all_feeds[random.randint(0,len(all_feeds)-1)],keyword = all_keywords[random.randint(0,len(all_keywords)-1)])) #TODO: Random Date ? 
      new_sents[i].save()  
   
  logger.info('All Sentiments are: '+str(Sentiment.objects.all()))

def populate_db(min_sentiment = 10, min_worker = 1, min_feeds = 1, min_keywords = 1):
  logger.info('Start populating database...')
  all_worker = Worker.objects.all()
  if all_worker.__len__() < min_worker:
    for i in range(0,min_worker-len(all_worker)):
      Worker(score = 10, blocked = False).save()  

  all_worker = Worker.objects.all()
  
  logger.info('All Worker are: '+str(all_worker))  

  all_feeds = Feed.objects.all()
  if all_feeds.__len__() < min_feeds:
    for i in range(len(all_feeds),min_feeds):
      Feed(title = 'myTitle'+str(i), link = 'myLink'+str(i), content = 'myContent'+str(i), pub_date = timezone.now()).save()
  
  all_feeds = Feed.objects.all()

  logger.info('All Feeds are: '+str(all_feeds))

  all_keywords = Keyword.objects.all()
  if all_keywords.__len__() < min_keywords:
    new_keywords = []
    for i in range(0,min_keywords-len(all_keywords)):
      new_keywords.append(Keyword(text='keyword'+str(i),category='C',score = 10))
      new_keywords[i].save()
      new_keywords[i].feed = all_feeds[0:random.randint(0,len(all_feeds)-1)]
      new_keywords[i].worker = all_worker[0:random.randint(0,len(all_worker)-1)]
      new_keywords[i].save()
  
  all_keywords = Keyword.objects.all()
  
  logger.info('All Keywords are: '+str(all_keywords))

  all_sentiments = Sentiment.objects.all()
  
  if len(all_sentiments) < min_sentiment:
    new_sents = []
    for i in range(0,min_sentiment-len(all_sentiments)):
      new_sents.append(Sentiment(score=random.randint(0,5),com_date = timezone.now(),worker = all_worker[random.randint(0,len(all_worker)-1)],feed = all_feeds[random.randint(0,len(all_feeds)-1)],keyword = all_keywords[random.randint(0,len(all_keywords)-1)])) #TODO: Random Date ? 
      new_sents[i].save()  
   
  logger.info('All Sentiments are: '+str(Sentiment.objects.all()))

