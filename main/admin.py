from django.contrib import admin
from .models import Profile, Department, Employer, MarkupType, Products, Photo, Options, Sale


class DepartmentInline(admin.TabularInline):
    fk_name = 'user'
    model = Department

class EmployerInline(admin.TabularInline):
    fk_name = 'user'
    model = Employer


class ProductsInline(admin.TabularInline):
    fk_name = 'user'
    model = Products


class PhotoInline(admin.TabularInline):
    fk_name = 'product'
    model = Photo


class OptionsInline(admin.TabularInline):
    fk_name = 'product'
    model = Options


class SaleInline(admin.TabularInline):
    fk_name = 'user'
    model = Sale


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline, EmployerInline, ProductsInline, SaleInline, ]


@admin.register(Products)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, OptionsInline, ]
