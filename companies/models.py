from django.db import models

# Create your models here.
NULL_BLANK = {'null': True, 'blank': True}


class DateModel(models.Model):
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Bank(DateModel):
    name = models.CharField(max_length=30)
    web_site = models.URLField(verbose_name='website')
    email = models.EmailField()

    def __str__(self):
        return self.name


class Company(DateModel):

    name = models.CharField(max_length=30)
    web_site = models.URLField(verbose_name='website')
    email = models.EmailField()
    logo = models.ImageField(upload_to='media/logos', blank=True, null=True)
    post_index = models.IntegerField(verbose_name='post index')
    bank = models.ManyToManyField(Bank)

    def __str__(self):
        return self.name
