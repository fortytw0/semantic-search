from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model) : 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=64 , unique=True, blank=False)
    search_string = models.CharField(max_length=64 , blank=False)
    filter_keywords = models.CharField(max_length=512)
    subreddits = models.CharField(max_length=512, blank=False)
    description = models.TextField()
    time_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.search_string