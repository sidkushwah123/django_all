from MarkupPy.markup import _oneliner
from django.db import models
from datetime import date
import django
from django.urls import reverse
from admin_manage_country.models import AwCountry
from admin_manage_producer.models import AwSetTo
from django.contrib.auth.models import User
from wineproject.utils import  slug_generator_for_AwRegion
from django.db.models.signals import pre_save
# Create your models here.

def user_directory_path(instance, filename):
    producer_id_in_list = instance.Region_Name.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format(producer_id_in_string+"/Region/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)

def user_directory_path_banner(instance, filename):
    producer_id_in_list = instance.Region_Name.split(" ")
    today_date = date.today()
    producer_id_in_string = '_'.join([str(elem) for elem in producer_id_in_list])
    return '{0}/{1}'.format(producer_id_in_string+"/Region/banner/"+str(today_date.year)+"/"+str(today_date.month)+"/"+str(today_date.day),filename)


class AwRegion(models.Model):
    Country = models.ForeignKey(AwCountry ,related_name='AwRegion_Country', on_delete=models.SET_NULL, null=True,blank=True)
    Region_Name = models.CharField(max_length=120,unique=True)
    Slug = models.CharField(max_length=120,unique=True,null=True,blank=True)
    Set_To = models.ManyToManyField(AwSetTo, blank=True, related_name='AwRegion_set_to')
    Region_Image = models.ImageField(upload_to=user_directory_path)
    banner_Image = models.ImageField(upload_to=user_directory_path_banner,null=True,blank=True)
    Short_Description = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Status = models.BooleanField(default=True)
    Created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='AwRegion_Created_by')
    Created_date = models.DateTimeField(default=django.utils.timezone.now)
    Updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='AwRegion_Updated_by')
    Updated_date = models.DateTimeField(default=django.utils.timezone.now)


    def get_absolute_url(self):
        return reverse('admin_manage_region:region')
    def __str__(self):
        return str(self.Region_Name)

    class Meta:
        verbose_name_plural = "AW Region"
def pre_save_create_slug(sender, instance, *args, **kwargs):
    if not instance.Slug:
        instance.Slug= slug_generator_for_AwRegion(instance)
pre_save.connect(pre_save_create_slug, sender=AwRegion)