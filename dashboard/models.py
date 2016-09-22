from django.db import models

# Create your models here.
class Todo(models.Model):
    todo_text = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    username = models.CharField(max_length=200, default='')

    def __str__(self):
       return self.todo_text + ":" + self.username

class Course(models.Model):
    def __init__(self, number, start, end):
        self.number = number
        self.start = start
        self.end = end

    def __str__(self):
        return self.number + " " + self.start + " "
