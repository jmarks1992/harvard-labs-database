from django.db import models

# Create your models here.

class Tags(models.Model):
   tag=models.CharField(max_length=30)
   
   class Meta:
      verbose_name_plural="Tags"
   
   
class Labs(models.Model):
   PI_email=models.EmailField()
   PI_name=models.CharField(max_length=50)
   building=models.CharField(max_length=50)
   department=models.CharField(max_length=50)
   funding_sources=models.CharField(max_length=70)
   lab_desc=models.CharField(max_length=5000)
   lab_location=models.CharField(max_length=50)
   lab_name=models.CharField(max_length=60)
   lab_url=models.URLField()
   n_members=models.CharField(max_length=10)
   pubmed_name=models.CharField(max_length=50)
   tags=models.ManyToManyField(Tags)
   def __unicode__(self):
      return u'%s Lab' % (self.PI_name)
   class Meta:
      verbose_name_plural="Labs"
   
