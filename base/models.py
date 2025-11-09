from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django_jalali.db import models as jmodels
from django.contrib.auth.hashers import make_password

# Create your models here.

phone_validator = RegexValidator(
    regex=r'^\d+$',
    message="Phone number must contain only digits"
)

float_validator = [MinValueValidator(0.0), MaxValueValidator(5.0)]

class Product(models.Model):
    # list of tuples
    Color = [
        ('0','سفید'),
        ('1','مشکی'),
        ('2','آبی'),
        ('3','قرمز'),
    ]
    # fields
    title = models.CharField(max_length=200, verbose_name="عنوان", null=True)
    describtion = models.TextField(max_length=2000, verbose_name="توضیحات", null=True)
    price = models.IntegerField(verbose_name="قیمت", null=True)
    image = models.ImageField(verbose_name="تصویر", null=True)
    productFeatures = models.ManyToManyField('ProductFeatures', related_name='products', verbose_name="ویژگی")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='products', verbose_name="دسته بندی", null=True)
    color = models.CharField(max_length=1, choices=Color, verbose_name="رنگ", null=True)
    is_available = models.BooleanField(verbose_name="موجودی")
    rate = models.FloatField(validators=float_validator, verbose_name="امتیاز", null=True)
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    @property
    def final_price(self):
        if self.discount > 0:
            return round(self.price * (1 - self.discount/100))
        return self.price


    def __str__(self):
        return self.title
    
class ProductFeatures(models.Model):
    title = models.CharField(max_length=127, null=True, verbose_name='عنوان')
    amount = models.CharField(max_length=127, null=True, verbose_name='مقدار')
    def __str__(self):
        return f"{self.title} {self.amount}"
    
    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
    
class Person(AbstractUser):
    phone = models.CharField(max_length=13, null=True, validators=[phone_validator], verbose_name='تلفن', blank=True)
    code = models.CharField(max_length=13, null=True, verbose_name='کد ملی', blank=True)
    birthDate = jmodels.jDateTimeField(null=True, verbose_name='تاریخ تولد', blank=True)


    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'شخص'
        verbose_name_plural = 'اشخاص'


    def __str__(self):
        return self.username
    
class Comment(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=2047, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='comments')
    date = jmodels.jDateTimeField(null=True, verbose_name='تاریخ', blank=True)
    rate = models.FloatField(validators=float_validator, verbose_name="امتیاز", null=True)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

class Category(models.Model):
    title = models.CharField(max_length=127, null=True, verbose_name='عنوان')
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'