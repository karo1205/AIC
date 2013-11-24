from django.db import models
import datetime


class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    content = models.TextField()

    def __unicode__(self):
        return self.title


class Keyword(models.Model):
    text = models.CharField(max_length=500)


class Worker(models.Model):
    score = models.IntegerField(default=0)
    blocked = models.BooleanField('blocked')
    worker_uri = models.CharField(max_length=200, default='NULL')


class Task(models.Model):
    STATUS_CHOICES = (
	('N', 'new'),
	('S', 'started'),
	('D', 'done'),
    ('P', 'processed')
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='N')
    pub_date = models.DateTimeField('date publisheid', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    com_date = models.DateTimeField('date completed', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
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


# Create your models here.
