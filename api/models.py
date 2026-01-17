from django.db import models

class JDmodel(models.Model):
    text = models.TextField()
    role = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.role