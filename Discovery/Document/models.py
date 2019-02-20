from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
import os

# Create your models here.

class Config(models.Model):
    url = models.CharField(max_length=250)
    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "{0}. {1}".format(self.id, self.url)
        # return "(ID:%s)" % (self.id)

class Article(models.Model):
    csvFile = models.FileField(upload_to='Document/csv', verbose_name="")
    # description = models.CharField(max_length=255, blank=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    opening_text = models.TextField(blank=True)
    source = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    subregion = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)
    article_content = models.TextField(blank=True)
    english_translation = models.TextField(blank=True)
    sentiment_score = models.FloatField(null=True, blank=True, default=None)
    concept_json = models.TextField(blank=True)

    @property
    def filename(self):
        return os.path.basename(self.csvFile.name)

    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "{0}. {1} - {2}".format(self.id, self.headline, self.source)
        # return "(ID:%s)" % (self.id) 
