from django_cron import CronJobBase, Schedule
from analysis.models import Feed, Task, Worker, Keyword, Sentiment
from analysis.utils import *
#from django.core.files import File
#import datetime
from django.utils import timezone
import feedparser
import json
import urllib2
import requests
import logging
logger = logging.getLogger(__name__)


class Fetch_Feeds(CronJobBase):

    """
    Docstring.

    """

    RUN_EVERY_MINS = 3  # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'analysis.fetch_feeds'    # a unique code

    def do(self):
        logger.info("Getting Feeds")
        d = feedparser.parse('http://ftr.fivefilters.org/makefulltextfeed.php?url=http%3A%2F%2Ffeeds.finance.yahoo.com%2Frss%2F2.0%2Fheadline%3Fs%3Dyhoo%2Cmsft%2Ctivo%26region%3DUS%26lang%3Den-US&max=3')
#        d = feedparser.parse('http://derstandard.at/?page=rss')
        for item in d.entries:
            if Feed.objects.filter(link=item.id):
                logger.info("feed already in db: " + item.id)
                pass
            else:
                f = Feed(link=item.id, title=item.title, content=item.summary_detail.value)
                # pub_date=datetime.fromtimestamp(mktime(item.published_parsed)
                f.save()
                logger.info("new feed was stored: " + item.id)
                t = Task(pub_date=timezone.now(), question='Question1', feed=f)
                t.save()
                logger.info("new task was stored")
                payload = json.load(urllib2.urlopen('http://127.0.0.1:8002/api/v1/task/1/?format=json'))
                payload['data'] = json.dumps(transform_task_to_data(t))
                payload['price'] = 0
                payload['question'] = 'Please find keywords in this text'
                #TODO: callback uri
                payload['callback_uri'] = 'http://127.0.0.1:8000/api/v1/task/'+ str(t.id) +'/'
                payload['keyword_count'] = 5
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


class Get_Tasks(CronJobBase):

    """
    This cronjobs checks periodicall on undone tasks in the Tasks table und requests the actual status from the
    crowdsourcing plattform.
    """

    RUN_EVERY_MINS = 3  # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'analysis.get_tasks'    # a unique code

    def do(self):
        logger.info('Getting open tasks from DB')
        opentasks = Task.objects.filter(status='S')  # get all started tasks

        for t in opentasks:
            payload = json.load(urllib2.urlopen(t.task_uri + '?format=json'))
            logger.info("Checking: " + payload['resource_uri'])
            if payload['answer'] != 'NULL':  # save answer when there is one
                t.answer = payload['answer']
                t.status = 'D'  # set to to done (enable for processeing)
                try:  # see of worker alread is known
                    w = Worker.objects.get(worker_uri=payload['worker'])
                    t.worker_id = w.id  # set Task-Worker realtion
                    logger.info("worker is already known: id = " + str(w.id))
                    logger.info("worker " + str(w.id) + " did task " + str(t.id))
                except Worker.DoesNotExist:
                    # create new worker
                    newworker = Worker(worker_uri=payload['worker'])
                    newworker.save()  # save befor assigning to t becasue newworker hast'got an id yet
                    t.worker_id = newworker.id
                    logger.info("new worker created: id = " + str(newworker.id))
                    logger.info("worker " + str(newworker.id) + " did task " + str(t.id))
                t.save()
        """
        Process Task Type 1

        """

        opentasks = Task.objects.filter(status='D')  # get all started tasks
        logger.info('Getting done tasks from DB. ' + str(opentasks.count()) + ' elements found')
        for t in opentasks:
            logger.info("Processing Task " + str(t.id))
            try:
                #answer = json.loads(t.answer)
                answer = t.answer  #TODO replace all anser with t.answer
            except ValueError:
                logger.error("the answer field of task " + str(t.id) + " does not contain a valid JSON Format. Skipping.")
                continue    # if there is not valid JSON there is no pint of considerung this answer
                            # TODO: Implement quality control and pot task
                            # again

            for kw in answer['keywords'].keys():
                try:
                    keyword = Keyword.objects.get(text=kw)
                    logger.info('Keyword "' + kw + '" already in DB')
                    t.keywords.add(keyword)
                    logger.info('Keyword "' + kw + '" assigned to Task' + str(t.id))
                except Keyword.DoesNotExist:
                    newkeyword=Keyword(text=str(kw), category=answer['keywords'][kw])
                    newkeyword.save()
                    t.keywords.add(newkeyword)
                    logger.info('new keyword "' + kw + '" created and assigned to Task' + str(t.id))

            t.status='P'  # set status to processed
            t.save()

