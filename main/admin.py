from django.contrib import admin
from .models import Profile, Department, Employer, Products, Photo, Options, Sales, Returns, Markups


class DepartmentInline(admin.TabularInline):
    fk_name = 'user'
    model = Department


class EmployerInline(admin.TabularInline):
    fk_name = 'user'
    model = Employer


class MarkupsInline(admin.TabularInline):
    fk_name = 'user'
    model = Markups


class ProductsInline(admin.TabularInline):
    fk_name = 'user'
    model = Products


class PhotoInline(admin.TabularInline):
    fk_name = 'product'
    model = Photo


class OptionsInline(admin.TabularInline):
    fk_name = 'product'
    model = Options


class SalesInline(admin.TabularInline):
    fk_name = 'user'
    model = Sales


class ReturnsInline(admin.TabularInline):
    fk_name = 'user'
    model = Returns


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline, EmployerInline, MarkupsInline, ProductsInline, SalesInline, ReturnsInline]


@admin.register(Products)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, OptionsInline, ]
