from django.db import models

# Create your models here.

class Config(models.Model):
    url = models.CharField(max_length=250)
    def __str__(self):
        # return self.contract_title
        # return "%s (ID:%s)" % (self.name, self.id)
        return "{0}. {1}".format(self.id, self.url)
        # return "(ID:%s)" % (self.id) 