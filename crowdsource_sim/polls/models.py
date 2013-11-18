from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    content = models.TextField()

class Keyword(models.Model):
    text = models.CharField(max_length=500)

class Worker(models.Model):
    score = models.IntegerField(default=0)
    blocked = models.BooleanField('blocked')

class Task(models.Model):
    price = models.IntegerField(default=0)
    callback_uri = models.CharField(max_length=200)
    question = models.TextField()
    answer = models.TextField()
    feed = models.ForeignKey(Feed)
    keywords = models.ManyToManyField(Keyword)
    worker = models.ForeignKey(Worker)

# Create your models here.
