from django.db import models

# Create your models here.


class BlogAdminAdd(models.Model):
    class Meta:
        verbose_name = "添加博客"
        verbose_name_plural = verbose_name


class BlogAdminUpdate(models.Model):
    class Meta:
        verbose_name = "更改博客"
        verbose_name_plural = verbose_name

