from django.db import models


class Resume(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
