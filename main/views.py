from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
import json
import base64
from PIL import Image
import io
import os

from .serializers import UserSerializer
from .forms import UserRegistrationForm
from .models import Department, Employer, Markups, Products, Sales, Photos, Options, Sales, Returns


def qr_to_json(file):
    path_to_file = str(file)
    data = {}
    with open(path_to_file, mode='rb') as file:
        img = file.read()
    file_name = os.path.basename(path_to_file)
    data['file_name'] = file_name
    data['image'] = base64.b64encode(img).decode('utf-8')
    return data


def png_to_json(path_to_file):
    data = {}
    with open(str(path_to_file), mode='rb') as file:
        img = file.read()
    file_name = str(path_to_file).split('/')[-1]
    data['file_name'] = file_name
    data['image'] = base64.b64encode(img).decode('utf-8')
    return data


def json_to_png(data, output_file):
    image_data = data['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    image.save(output_file)
    return image


def all_data():
    queryset = User.objects.all()

    serializer_for_queryset = UserSerializer(
        instance=queryset,
        many=True
    )
    data = serializer_for_queryset.data
    for item in data:
        user = User.objects.get(username=item['email'])

        try:
            departments = user.profile.departments.all()
            item['departments'] = [{"building": department.building, "level": department.level, "line": department.line, "department": department.department}
                              for department in departments]
        except:
            item['departments'] = []

        try:
            employees = user.profile.employees.all()
            item['employees'] = [{"name": employer.name, "post": employer.post, "status": employer.status}
                              for employer in employees]
        except:
            item['employees'] = []

        try:
            markups = user.profile.markups.all()
            item['markups'] = [{"name": markup.name, "price_range_from": markup.price_range_from, "price_range_to": markup.price_range_to,
                                "markup": markup.markup, "markup_method": markup.markup_method}
                              for markup in markups]
        except:
            item['markups'] = []

        try:
            products = user.profile.products.all()
            item['products'] = [{"uid": product.uid, "qr_code": qr_to_json(product.qr_code), "name": product.name, "quantity": product.quantity,
                                 "description": product.description, "price_purchasing": product.price_purchasing,
                                 "price_retail": product.price_retail, "price_wholesale": product.price_wholesale, "price_agent": product.price_agent,
                                 "photos": [png_to_json(photo) for photo in product.photos.all()] if product.photos.all() else [],
                                 "options": [{"color": option.color, "size": option.size, "quantity": option.quantity, "storage": option.storage,
                                 "price_purchasing": option.price_purchasing, "price_retail": option.price_retail, "price_wholesale": option.price_wholesale,
                                 "price_agent": option.price_agent} for option in product.options.all()] if product.options.all() else []} for product in products]
        except:
            item['products'] = []

        try:
            sales = user.profile.sales.all()
            item['sales'] = [{"date_time": sale.date_time.strftime("%d.%m.%y %H:%M"), "photo": png_to_json(sale.photo), "name": sale.name,
                              "color": sale.color, "size": sale.size, "quantity": sale.quantity,
                              "sale_sum": sale.sale_sum, "employer": sale.employer} for sale in sales]
        except:
            item['sales'] = []

        try:
            returns = user.profile.returns.all()
            item['returns'] = [{"date_time": return_obj.date_time.strftime("%d.%m.%y %H:%M"), "photo": png_to_json(return_obj.photo), "name": return_obj.name,
                              "color": return_obj.color, "size": return_obj.size, "quantity": return_obj.quantity,
                              "sale_sum": return_obj.sale_sum, "employer": return_obj.employer} for return_obj in returns]
        except:
            item['returns'] = []


    return serializer_for_queryset.data


def user_data(email):
    user = User.objects.get(username=email)
    serializer_for_queryset = UserSerializer(
        instance=user,
    )
    item = serializer_for_queryset.data
    try:
        departments = user.profile.departments.all()
        item['departments'] = [{"building": department.building, "level": department.level, "line": department.line, "department": department.department}
                          for department in departments]
    except:
        item['departments'] = []

    try:
        employees = user.profile.employees.all()
        item['employees'] = [{"name": employer.name, "post": employer.post, "status": employer.status}
                          for employer in employees]
    except:
        item['employees'] = []

    try:
        markups = user.profile.markups.all()
        item['markups'] = [{"name": markup.name, "price_range_from": markup.price_range_from, "price_range_to": markup.price_range_to,
                            "markup": markup.markup, "markup_method": markup.markup_method}
                          for markup in markups]
    except:
        item['markups'] = []

    try:
        products = user.profile.products.all()
        item['products'] = [{"uid": product.uid, "qr_code": qr_to_json(product.qr_code), "name": product.name, "quantity": product.quantity,
                             "description": product.description, "price_purchasing": product.price_purchasing,
                             "price_retail": product.price_retail, "price_wholesale": product.price_wholesale, "price_agent": product.price_agent,
                             "photos": [png_to_json(photo) for photo in product.photos.all()] if product.photos.all() else [],
                             "options": [{"color": option.color, "size": option.size, "quantity": option.quantity, "storage": option.storage,
                             "price_purchasing": option.price_purchasing, "price_retail": option.price_retail, "price_wholesale": option.price_wholesale,
                             "price_agent": option.price_agent} for option in product.options.all()] if product.options.all() else []} for product in products]
    except:
        item['products'] = []

    try:
        sales = user.profile.sales.all()
        item['sales'] = [{"date_time": sale.date_time.strftime("%d.%m.%Y %H:%M"), "photo": png_to_json(sale.photo), "name": sale.name,
                          "color": sale.color, "size": sale.size, "quantity": sale.quantity,
                          "sale_sum": sale.sale_sum, "employer": sale.employer} for sale in sales]
    except:
        item['sales'] = []

    try:
        returns = user.profile.returns.all()
        item['returns'] = [{"date_time": return_obj.date_time.strftime("%d.%m.%Y %H:%M"), "photo": png_to_json(return_obj.photo), "name": return_obj.name,
                          "color": return_obj.color, "size": return_obj.size, "quantity": return_obj.quantity,
                          "sale_sum": return_obj.sale_sum, "employer": return_obj.employer} for return_obj in returns]
    except:
        item['sales'] = []


    return item


class GetAllInfoView(APIView):
    def get(self, request):
        return Response(all_data())


class GetUserInfoView(APIView):
    def get(self, request, email):
        return Response(user_data(email))


class GetUserDepartmentsView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['departments'])


class GetUserEmployeesView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['employees'])


class GetUserMarkupsView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['markups'])


class GetUserProductsView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['products'])


class GetUserSalesView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['sales'])


class GetUserReturnsView(APIView):
    def get(self, request, email):
        return Response(user_data(email)['returns'])


class GetProductView(APIView):
    def get(self, request, uid):
        product = Products.objects.get(uid=uid)
        data = {
            "email": product.user.user.username,
            "uid": product.uid,
            "qr_code": qr_to_json(product.qr_code),
            "name": product.name,
            "quantity": product.quantity,
            "description": product.description,
            "price_purchasing": product.price_purchasing,
            "price_retail": product.price_retail,
            "price_wholesale": product.price_wholesale,
            "price_agent": product.price_agent,
            "photos": [png_to_json(photo) for photo in product.photos.all()] if product.photos.all() else [],
            "options": [{"color": option.color, "size": option.size, "quantity": option.quantity, "storage": option.storage,
            "price_purchasing": option.price_purchasing, "price_retail": option.price_retail, "price_wholesale": option.price_wholesale,
            "price_agent": option.price_agent} for option in product.options.all()] if product.options.all() else []
        }
        return Response(data)


class AddUserView(APIView):
    def get(self, request, data):
        if data:
            data_dict = json.loads(data)
            user_form = UserRegistrationForm({'username': data_dict['email'], 'password': data_dict['password']})
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                new_user.profile.name = data_dict['name']
                new_user.profile.balance = data_dict['balance']
                new_user.profile.status = data_dict['status']
                new_user.save()
                return Response({"status": "successfully"})
            else:
                return Response({"error": user_form.errors})
        return Response({"error": "No data received!"})


class AddUserDepartmentView(APIView):
    def get(self, request, email, data):
        try:
            user = User.objects.get(username=email)
        except:
            return Response({'error': "There is no such user"})
        if data:
            data_dict = json.loads(data)
            building = data_dict['building']
            level = data_dict['level']
            line = data_dict['line']
            department = data_dict['department']
            if building and level and line and department:
                new_department = Department()
                new_department.user = user.profile
                new_department.building = building
                new_department.level = level
                new_department.line = line
                new_department.department = department
                for i in user.profile.departments.all():
                    if str(i) == str(new_department):
                        return Response({"error": "Such a department already exists at this vendor"})
                new_department.save()
                return Response({"status": "successfully"})
            else:
                return Response({"error": "No data received!"})
        return Response({"error": "No data received!"})


class AddUserEmployeeView(APIView):
    def get(self, request, email, data):
        try:
            user = User.objects.get(username=email)
        except:
            return Response({'error': "There is no such user"})
        if data:
            data_dict = json.loads(data)
            name = data_dict['name']
            post = data_dict['post']
            status = data_dict['status']
            if name and post and status:
                new_employer = Employer()
                new_employer.user = user.profile
                new_employer.name = name
                new_employer.post = post
                new_employer.status = status
                for i in user.profile.employees.all():
                    i_dict = {
                        'name': i.name,
                        'post': i.post,
                        'status': str(i.status),
                    }
                    if i_dict == data_dict:
                        return Response({"error": "Such a employer already exists at this vendor"})
                new_employer.save()
                return Response({"status": "successfully"})
            else:
                return Response({"error": "No data received!"})
        return Response({"error": "No data received!"})


class AddUserMarkupView(APIView):
    def get(self, request, email, data):
        try:
            user = User.objects.get(username=email)
        except:
            return Response({'error': "There is no such user"})
        if data:
            data_dict = json.loads(data)
            name = data_dict['name']
            price_range_from = data_dict['price_range_from']
            price_range_to = data_dict['price_range_to']
            markup = data_dict['markup']
            markup_method = data_dict['markup_method']
            if name and price_range_from and price_range_to and markup and markup_method:
                new_markup = Markups()
                new_markup.user = user.profile
                new_markup.name = name
                new_markup.price_range_from = price_range_from
                new_markup.price_range_to = price_range_to
                new_markup.markup = markup
                new_markup.markup_method = markup_method
                for i in user.profile.markups.all():
                    i_dict = {
                        'name': i.name,
                        'price_range_from': str(i.price_range_from),
                        'price_range_to': str(i.price_range_to),
                        'markup': str(i.markup),
                        'markup_method': i.markup_method,
                    }
                    if i_dict == data_dict:
                        return Response({"error": "Such a markup already exists at this vendor"})
                new_markup.save()
                return Response({"status": "successfully"})
            else:
                return Response({"error": "No data received!"})
        return Response({"error": "No data received!"})


class AddUserProductView(APIView):
    def get(self, request, email, data):
        try:
            user = User.objects.get(username=email)
        except:
            return Response({'error': "There is no such user"})
        if data:
            data_dict = json.loads(data)
            uid = data_dict['uid']
            name = data_dict['name']
            quantity = data_dict['quantity']
            description = data_dict['description']
            price_purchasing = data_dict['price_purchasing']
            price_retail = data_dict['price_retail']
            price_wholesale = data_dict['price_wholesale']
            price_agent = data_dict['price_agent']
            if uid and name and quantity and description and price_purchasing and price_agent and price_retail and price_wholesale:
                new_product = Products()
                new_product.user = user.profile
                new_product.uid = uid
                new_product.name = name
                new_product.quantity = quantity
                new_product.description = description
                new_product.price_purchasing = price_purchasing
                new_product.price_retail = price_retail
                new_product.price_wholesale = price_wholesale
                new_product.price_agent = price_agent
                for i in Products.objects.all():
                    if str(i.uid) == str(data_dict['uid']):
                        return Response({"error": "Such a product already exists at this vendor"})
                new_product.save()
                try:
                    for photo in data_dict['photos']:
                        new_photo = Photos()
                        new_photo.product = new_product
                        new_photo.photo = json_to_png(photo["image"], f'main/static/png/products/{user.username}/{uid} ({name})/{photo["file_name"]}')
                        new_photo.save()
                except:
                    pass

                try:
                    for option in data_dict['options']:
                        new_option = Options()
                        new_option.product = new_product
                        new_option.color = option['color']
                        new_option.size = option['size']
                        new_option.quantity = option['quantity']
                        new_option.storage = option['storage']
                        new_option.price_purchasing = option['price_purchasing']
                        new_option.price_retail = option['price_retail']
                        new_option.price_wholesale = option['price_wholesale']
                        new_option.price_agent = option['price_agent']
                        new_option.save()
                except:
                    pass
                return Response({"status": "successfully"})
            else:
                return Response({"error": "No data received!"})
        return Response({"error": "No data received!"})