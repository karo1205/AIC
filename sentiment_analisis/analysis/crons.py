from django_cron import CronJobBase, Schedule
from analysis.models import Feed, Task
#from django.core.files import File
import datetime
import feedparser
import json
import urllib2

import logging
logger = logging.getLogger(__name__)


class Fetch_Feeds(CronJobBase):

    """
    Docstring.

    """

    RUN_EVERY_MINS = 5  # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'analysis.fetch_feeds'    # a unique code

    def do(self):
#        d = feedparser.parse('http://ftr.fivefilters.org/makefulltextfeed.php?url=http%3A%2F%2Ffeeds.finance.yahoo.com%2Frss%2F2.0%2Fheadline%3Fs%3Dyhoo%2Cmsft%2Ctivo%26region%3DUS%26lang%3Den-US&max=3')
        d = feedparser.parse('http://derstandard.at/?page=rss')
        for item in d.entries:
            print item.id
            if Feed.objects.filter(link=item.id):
                pass
            else:
                f = Feed(link=item.id, title=item.title, content=item.summary_detail.value)
                f.save()
                logger.info("new feed was stored")
                t = Task(pub_date=datetime.datetime.now(), question='Question1', feed=f.id)
                t.save()
                #TODO: fill data field
                logger.info("new task was stored")
                post = json.load(urllib2.urlopen('http://127.0.0.1:8001/api/v1/task/1/?format=json'))
                post['data'] = f.content
                post['price'] = 0
                post['question'] = 'Please find keywords in this text'
                post['callback_uri'] = 'testdata'
                post['answer'] = ''
                logger.info(post)


class Get_Tasks(CronJobBase):

    """
    This cronjobs checks periodicall on undone tasks in the Tasks table und requests the actual status from the
    crowdsourcing plattform.
    """

    RUN_EVERY_MINS = 5  # every 5 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'analysis.get_tasks'    # a unique code

    def do(self):
        pass
