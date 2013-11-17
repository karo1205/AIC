from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField()
    content = models.TextField()

class Keyword(models.Model):
    text = models.CharField(max_length=500)

class Worker(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    blocked = models.BooleanField('blocked')

    def __unicode__(self):
        return self.name

class Task(models.Model):
    price = models.IntegerField(default=0)
    callback_uri = models.CharField(max_length=200)
    question = models.TextField()
    answer = models.TextField(default = 'NULL')
    data = models.TextField(default = 'NULL')
  #  keywords = models.ManyToManyField(Keyword)
    worker = models.ForeignKey(Worker)

    def __unicode__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.worker_id = 1

        super(Task, self).save(*args, **kwargs)
