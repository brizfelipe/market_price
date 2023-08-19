from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=256)
    code = models.IntegerField()
    img_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Stores'
        indexes = [
            models.Index(fields=['code']),
        ]


class Department(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    cod = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    image_link = models.URLField()
    class Meta:
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['cod']),
        ]


class Aisle(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    cod = models.CharField(max_length=256)
    image_link = models.URLField()
    class Meta:
        verbose_name_plural = 'Aisles'
        indexes = [
            models.Index(fields=['cod']),
        ]


class Product(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    package = models.CharField(max_length=256,null=True, blank=True)
    image_link = models.URLField()
    class Meta:
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name']),
        ]


class Price_product_history(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    consultation_date = models.DateTimeField(auto_now_add=True)
    consultation_day = models.IntegerField()
    consultation_month = models.IntegerField()
    consultation_year = models.IntegerField()
    consultation_weekNumber = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Price_product_history'
        indexes = [
            models.Index(fields=['product']),
        ]