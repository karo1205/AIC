from django.db import models
from django.forms import ModelForm


# Create your models here.


class Poll(models.Model):

    """Poll Class."""

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.question


class Choice(models.Model):

    """Choice Class."""

    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class PollForm(ModelForm):

    """This is a ModelForm for the Poll Class."""

    class Meta:
        model = Poll
        fields = ['question', 'pub_date']
