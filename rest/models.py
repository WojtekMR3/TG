from django.db import models

# Create your models here.
class World(models.Model):
    name = models.CharField(max_length=16)
    onlineCount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [models.Index(fields=['created_at', ]), ]

class Highscore(models.Model):
    nick = models.CharField(max_length=30)
    world = models.CharField(max_length=16)
    vocation = models.CharField(max_length=15)
    level = models.IntegerField()
    exp = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)