from django.db import models


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
    pub_date = models.DateTimeField('date published')
    com_date = models.DateTimeField('date completed')
    orphaned = models.BooleanField('Orphaned')
    price = models.IntegerField(default=0)
    callback_uri = models.CharField(max_length=200)
    question = models.TextField()
    answer = models.TextField()
    feed = models.ForeignKey(Feed)
    keywords = models.ManyToManyField(Keyword)
    worker = models.ForeignKey(Worker)


class Sentiment(models.Model):
    keyword = models.ForeignKey(Keyword)
    worker = models.ForeignKey(Worker)
    score = models.IntegerField(default=0)


# Create your models here.
