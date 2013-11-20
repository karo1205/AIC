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


class Task(models.Model):
    STATUS_CHOICES = (
	('NS', 'not started'),
	('S', 'started'),
	('D', 'done')
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='NS')
    pub_date = models.DateTimeField('date publishe    com_date = models.DateTimeField('date completed', default=datetime.datetime(2000, 1, 1, 1, 1, 1))
    orphaned = models.BooleanField('Orphaned',default=price = models.IntegerField(default=0)
    callback_uri = models.CharField(max_length=200, default='NULL')
    question = models.TextField()
    answer = models.TextField(default='NULL')
    feed = models.ForeignKey(Feed)
    keywords = models.ManyToManyField(Keyword)
    worker = models.ForeignKey(Worker, default=0) #TODO many to many relation


class Sentiment(models.Model):
    keyword = models.ForeignKey(Keyword)
    worker = models.ForeignKey(Worker)
    score = models.IntegerField(default=0)


# Create your models here.
