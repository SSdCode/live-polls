from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Question(models.Model): 
    sno= models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    livestatus = models.BooleanField(default=True)
    publicstatus = models.CharField(max_length=50)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text