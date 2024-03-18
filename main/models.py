from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    name = models.CharField("Имя", max_length=40, blank=True)
    balance = models.CharField("Баланс", max_length=40, blank=True)
    status = models.CharField("Статус", max_length=40, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Department(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="departments")
    building = models.CharField("Здание", max_length=40, blank=True)
    level = models.CharField("Этаж", max_length=40, blank=True)
    line = models.CharField("Линия", max_length=40, blank=True)
    department = models.CharField("Отдел", max_length=40, blank=True)

    def __str__(self):
        return f"{self.user.user.username}: {self.building} {self.level} {self.line} {self.department}"


class Employer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField("Имя", max_length=35, blank=True)
    post = models.CharField("Должность", max_length=35, blank=True)
    status = models.IntegerField("Статус", blank=True)

    def __str__(self):
        return self.name


class Markups(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="markups")
    name = models.CharField("Название наценки", max_length=50, blank=True)
    price_range_from = models.IntegerField("Диапазон цен от", blank=True)
    price_range_to = models.IntegerField("Диапазон цен до", blank=True)
    markup = models.IntegerField("Наценка", blank=True)
    markup_method = models.CharField("Способ наценки", max_length=20, blank=True)


class Products(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="products")
    uid = models.IntegerField("Артикул", blank=True)
    qr_code = models.ImageField("Фото", blank=True)
    name = models.CharField("Название", max_length=175, blank=True)
    quantity = models.IntegerField("Количество", blank=True)
    description = models.TextField("Описание")
    price_purchasing = models.IntegerField("Цена закупочная", blank=True)
    price_retail = models.IntegerField("Цена розница", blank=True)
    price_wholesale = models.IntegerField("Цена оптовая", blank=True)
    price_agent = models.IntegerField("Цена cвоим", blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            img = qrcode.make(f'https://get/product_by_uid/{self.uid}')
            qr_bytes = BytesIO()
            img.save(qr_bytes, format='PNG')
            self.qr_code.save(f"main/static/png/products_qr/{self.uid}.png", ContentFile(qr_bytes.getvalue()))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.uid} ({self.name})'


def photo_save(instance, filename):
    if not os.path.exists(f'main/static/png/products/{instance.product.user.user.username}/{instance.product.uid} ({instance.product.name})/{filename}'):
        return f'main/static/png/products/{instance.product.user.user.username}/{instance.product.uid} ({instance.product.name})/{filename}'


class Photos(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField("Фото", upload_to=photo_save)

    def __str__(self):
        return f'{self.photo}'


class Options(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="options")
    color = models.CharField("Цвет", max_length=50, blank=True)
    size = models.CharField("Размер", max_length=30, blank=True)
    quantity = models.IntegerField("Кол-во", blank=True)
    storage = models.CharField("Где лежит", max_length=50, blank=True)
    price_purchasing = models.IntegerField("Цена закупочная", blank=True)
    price_retail = models.IntegerField("Цена розница", blank=True)
    price_wholesale = models.IntegerField("Цена оптовая", blank=True)
    price_agent = models.IntegerField("Цена cвоим", blank=True)

    def __str__(self):
        return f'{self.color} {self.size}'


def sale_photo_save(instance, filename):
    return f'main/static/png/sales/{instance.user.user.username}/{instance.name} - {instance.date_time.strftime("%d.%m.%y %H:%M")}/{filename}'


class Sales(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sales")
    date_time = models.DateTimeField("Дата-время", blank=True)
    photo = models.ImageField("Фото", upload_to=sale_photo_save)
    name = models.CharField("Название", max_length=175, blank=True)
    color = models.CharField("Цвет", max_length=50, blank=True)
    size = models.CharField("Размер", max_length=30, blank=True)
    quantity = models.IntegerField("Кол-во", blank=True)
    price = models.IntegerField("Цена", blank=True)
    sale_sum = models.IntegerField("Сумма", blank=True)
    employer = models.CharField("Сотрудник", max_length=50, blank=True)

    def __str__(self):
        return f'{self.name} - {self.date_time}'


def return_photo_save(instance, filename):
    return f'main/static/png/returns/{instance.user.user.username}/{instance.name} - {instance.date_time.strftime("%d.%m.%y %H:%M")}/{filename}'


class Returns(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="returns")
    date_time = models.DateTimeField("Дата-время", blank=True)
    photo = models.ImageField("Фото", upload_to=return_photo_save)
    name = models.CharField("Название", max_length=175, blank=True)
    color = models.CharField("Цвет", max_length=50, blank=True)
    size = models.CharField("Размер", max_length=30, blank=True)
    quantity = models.IntegerField("Кол-во", blank=True)
    price = models.IntegerField("Цена", blank=True)
    sale_sum = models.IntegerField("Сумма", blank=True)
    employer = models.CharField("Сотрудник", max_length=50, blank=True)

    def __str__(self):
        return f'{self.name} - {self.date_time}'
