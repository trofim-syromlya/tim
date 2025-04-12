from django.db import models
from django.contrib.auth.models import User

class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)

    def total_answers(self):
        return self.correct_answers + self.incorrect_answers

    def correct_percentage(self):
        total = self.total_answers()
        if total == 0:
            return 0
        return (self.correct_answers / total) * 100

    def incorrect_percentage(self):
        total = self.total_answers()
        if total == 0:
            return 0
        return (self.incorrect_answers / total) * 100
