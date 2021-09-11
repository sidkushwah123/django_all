from django.db import models
import django
from django.contrib.auth.models import User
from django.urls import reverse
from wineproject.utils import  slug_generator_for_AwClassification
from django.db.models.signals import pre_save
# Create your models here.

class AwClassification(models.Model):
    Classification_Name = models.CharField(max_length=120,unique=True)
    Slug = models.CharField(max_length=120,unique=True,null=True,blank=True)
    Status = models.BooleanField(default=True)
    Created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='AwClassification_Created_by')
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='AwClassification_Updated_by')
    Updated_date = models.DateTimeField(default=django.utils.timezone.now)


    def __str__(self):
        return str(self.Classification_Name)
    class Meta:
        verbose_name_plural = "Aw Classification"

    def get_absolute_url(self):
        return reverse('admin_manage_classification:classification')
def pre_save_create_slug(sender, instance, *args, **kwargs):
    if not instance.Slug:
        instance.Slug= slug_generator_for_AwClassification(instance)
pre_save.connect(pre_save_create_slug, sender=AwClassification)