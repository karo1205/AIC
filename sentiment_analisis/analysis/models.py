from django.db import models
from django.utils import timezone
import datetime


class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    content = models.TextField()
    pub_date = models.DateTimeField('date published', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    def __unicode__(self):
        return self.title


class Keyword(models.Model):
    text = models.CharField(max_length=500)
    category = models.CharField(max_length=500,default='None')

    def __unicode__(self):
        return self.text


class Worker(models.Model):
    score = models.IntegerField(default=0)
    blocked = models.BooleanField('blocked')
    worker_uri = models.CharField(max_length=200, default='NULL')

class Order(models.Model):
    keyword = models.ForeignKey(Keyword)
    budgetlimit = models.IntegerField(default=0)
    start_date = models.DateTimeField('start date', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    end_date = models.DateTimeField('end date', default=datetime.datetime(2000, 1, 1, 1, 1, 1))

class Task(models.Model):
    STATUS_CHOICES = (
	('N', 'new'),
	('S', 'started'),
	('D', 'done'),
    ('P', 'processed')
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


class Sentiment(models.Model):
    keyword = models.ForeignKey(Keyword)
    worker = models.ForeignKey(Worker)
    score = models.IntegerField(default=0)
    feed = models.ForeignKey(Feed)
    com_date = models.DateTimeField('date completed', default=datetime.datetime(2000, 1, 1, 1, 1, 1))

# Create your models here.
