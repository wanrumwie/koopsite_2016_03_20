from django.db import models

class List(models.Model):
    list = models.TextField(default='', null=True)

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, null=True)

