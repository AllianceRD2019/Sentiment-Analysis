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

class InputFile(models.Model):
    csvFile = models.FileField(upload_to='Document/csv', verbose_name="")
    # description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.csvFile.name)

    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "{0}. {1}".format(self.id, self.filename)
        # return "(ID:%s)" % (self.id) 
