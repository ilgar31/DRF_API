from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
import json
import base64

from .serializers import UserSerializer
from .forms import UserRegistrationForm



def qr_to_json(file):
    path_to_file = "main/static/png/products_qr/" + str(file)
    data = {}
    with open(path_to_file, mode='rb') as file:
        img = file.read()
    data['image'] = base64.b64encode(img).decode('utf-8')
    return json.dumps(data)


def png_to_json(path_to_file):
    data = {}
    with open(str(path_to_file), mode='rb') as file:
        img = file.read()
    data['image'] = base64.b64encode(img).decode('utf-8')
    return json.dumps(data)


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
                                 "photos": [png_to_json(photo) for photo in product.photos.all()],
                                 "options": [{"color": option.color, "size": option.size, "quantity": option.quantity, "storage": option.storage,
                                 "price_purchasing": option.price_purchasing, "price_retail": option.price_retail, "price_wholesale": option.price_wholesale,
                                 "price_agent": option.price_agent} for option in product.options.all()]} for product in products]
        except:
            item['products'] = []

        try:
            sales = user.profile.sales.all()
            item['sales'] = [{"date_time": sale.date_time, "photo": png_to_json(sale.photo), "name": sale.name,
                              "color": sale.color, "size": sale.size, "quantity": sale.quantity,
                              "sale_sum": sale.sale_sum, "employer": sale.employer} for sale in sales]
        except:
            item['sales'] = []

        try:
            returns = user.profile.returns.all()
            item['returns'] = [{"date_time": return_obj.date_time, "photo": png_to_json(return_obj.photo), "name": return_obj.name,
                              "color": return_obj.color, "size": return_obj.size, "quantity": return_obj.quantity,
                              "sale_sum": return_obj.sale_sum, "employer": return_obj.employer} for return_obj in returns]
        except:
            item['sales'] = []


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
                             "photos": [png_to_json(photo) for photo in product.photos.all()],
                             "options": [{"color": option.color, "size": option.size, "quantity": option.quantity, "storage": option.storage,
                             "price_purchasing": option.price_purchasing, "price_retail": option.price_retail, "price_wholesale": option.price_wholesale,
                             "price_agent": option.price_agent} for option in product.options.all()]} for product in products]
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
        else:
            return Response({"error": "No data received!"})

