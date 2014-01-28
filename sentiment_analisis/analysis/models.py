
"""Docstring."""

from django.db import models
from django.utils import timezone
import datetime
# from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
import json
logger = logging.getLogger(__name__)


class Feed(models.Model):

    """Docstring."""

    title = models.CharField(max_length=500)
    link = models.URLField()
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=datetime.datetime(2000, 1, 1, 1, 1, 1))

    def __unicode__(self):
        return self.title


class Worker(models.Model):

    """Docstring."""

    score = models.IntegerField(default=0)
    blocked = models.BooleanField('blocked')
    worker_uri = models.CharField(max_length=200, default='NULL')

    def __unicode__(self):
        return self.worker_uri


class Keyword(models.Model):

    """Docstring."""

    text = models.CharField(max_length=500)
    category = models.CharField(max_length=500, default='None')
    worker = models.ManyToManyField(Worker)
    feed = models.ManyToManyField(Feed)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.text + "[" + self.category + "," + str(self.score) + "]"

    def get_sentiment_scores(self):
        data = []
        for sen in self.sentiment_set.values():
           data.append(int(sen["score"]))
        return data


class Order(models.Model):
    """Docstring."""

    budgetlimit = models.IntegerField(default=0)
    start_date = models.DateTimeField('start date', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    end_date = models.DateTimeField('end date', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    customer = models.CharField(max_length=500)
    keyword = models.ManyToManyField(Keyword)


class Sentiment(models.Model):

    """Docstring."""

    keyword = models.ForeignKey(Keyword)
    worker = models.ForeignKey(Worker)
    score = models.IntegerField(default=0)
    feed = models.ForeignKey(Feed)
    com_date = models.DateTimeField('date completed', default=timezone.now())


class Task(models.Model):

    """Docstring."""

    STATUS_CHOICES = (
	('N', 'new'),
	('S', 'started'),
	('D', 'done'),
    ('P', 'processed'),
    ('X', 'dead')
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='N')
    pub_date = models.DateTimeField('date publisheid', default=timezone.now())
    com_date = models.DateTimeField('date completed', default=timezone.now())
    orphaned = models.BooleanField('Orphaned',default=0)
    price = models.IntegerField(default=0)
    callback_uri = models.CharField(max_length=200, default='NULL')
    task_uri = models.CharField(max_length=200, default='NULL')
    question = models.TextField()
    answer = models.TextField(default='NULL')
    feed = models.ForeignKey(Feed)
    keywords = models.ManyToManyField(Keyword)
    worker = models.ForeignKey(Worker, default=0) #TODO many to many relation

    def __unicode__(self):
        return self.question

    def age_in_days(self):
        now = timezone.now()
        diff = now - self.pub_date
        return diff.days

def save_task_and_worker(sender, **kwargs):
    """Docstring."""

    logger.info('signal received')
    t = kwargs['instance']  # get task t from signal
    if t.status == 'D':
        logger.info('answer for task ' + str(t.id) + ' was recieved')
        t_answer = json.loads(t.answer)
        logger.info('worker' + t_answer['worker'] + ' did the work')
        post_save.disconnect(save_task_and_worker, sender=Task)
        try:  # see of worker alread is known
            w = Worker.objects.get(worker_uri=t_answer['worker'])  #TODO get worker URI
            t.worker_id = w.id  # set Task-Worker realtion
            logger.info("worker is already known: id = " + str(w.id))
            logger.info("worker " + str(w.id) + " did task " + str(t.id))
        except Worker.DoesNotExist:
            # create new worker
            newworker = Worker(worker_uri=t_answer['worker'])
            newworker.save()  # save befor assigning to t becasue newworker hast'got an id yet
            t.worker_id = newworker.id
            logger.info("new worker created: id = " + str(newworker.id))
            logger.info("worker " + str(newworker.id) + " did task " + str(t.id))
        t.save()
        post_save.connect(save_task_and_worker, sender=Task)

        process_task_answers()
post_save.connect(save_task_and_worker, sender=Task)

#at the end because of circular imports of models
from analysis.utils import *
