from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import json
import base64
from PIL import Image
import io
import os
import datetime

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


def json_to_bytes(data):
    image_bytes = base64.b64decode(data)
    return image_bytes


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
            item['departments'] = [{"id": department.id, "building": department.building, "level": department.level, "line": department.line, "department": department.department}
                              for department in departments]
        except:
            item['departments'] = []

        try:
            employees = user.profile.employees.all()
            item['employees'] = [{"id": employer.id, "name": employer.name, "post": employer.post, "status": employer.status}
                              for employer in employees]
        except:
            item['employees'] = []

        try:
            markups = user.profile.markups.all()
            item['markups'] = [{"id": markup.id, "name": markup.name, "price_range_from": markup.price_range_from, "price_range_to": markup.price_range_to,
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
            item['sales'] = [{"id": sale.id, "date_time": sale.date_time.strftime("%d.%m.%y %H:%M"), "photo": png_to_json(sale.photo), "name": sale.name,
                              "color": sale.color, "size": sale.size, "quantity": sale.quantity, "price": sale.price,
                              "sale_sum": sale.sale_sum, "employer": sale.employer} for sale in sales]
        except:
            item['sales'] = []

        try:
            returns = user.profile.returns.all()
            item['returns'] = [{"id": return_obj.id, "date_time": return_obj.date_time.strftime("%d.%m.%y %H:%M"), "photo": png_to_json(return_obj.photo), "name": return_obj.name,
                              "color": return_obj.color, "size": return_obj.size, "quantity": return_obj.quantity, "price": return_obj.price,
                              "sale_sum": return_obj.sale_sum, "employer": return_obj.employer} for return_obj in returns]
        except:
            item['returns'] = []


    return serializer_for_queryset.data


def user_data(pk):
    user = User.objects.get(id=pk)
    serializer_for_queryset = UserSerializer(
        instance=user,
    )
    item = serializer_for_queryset.data
    try:
        departments = user.profile.departments.all()
        item['departments'] = [{"id": department.id, "building": department.building, "level": department.level, "line": department.line, "department": department.department}
                          for department in departments]
    except:
        item['departments'] = []

    try:
        employees = user.profile.employees.all()
        item['employees'] = [{"id": employer.id, "name": employer.name, "post": employer.post, "status": employer.status}
                          for employer in employees]
    except:
        item['employees'] = []

    try:
        markups = user.profile.markups.all()
        item['markups'] = [{"id": markup.id, "name": markup.name, "price_range_from": markup.price_range_from, "price_range_to": markup.price_range_to,
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
        item['sales'] = [{"id": sale.id, "date_time": sale.date_time.strftime("%d.%m.%Y %H:%M"), "photo": png_to_json(sale.photo), "name": sale.name,
                          "color": sale.color, "size": sale.size, "quantity": sale.quantity,
                          "sale_sum": sale.sale_sum, "employer": sale.employer} for sale in sales]
    except:
        item['sales'] = []

    try:
        returns = user.profile.returns.all()
        item['returns'] = [{"id": return_obj.id, "date_time": return_obj.date_time.strftime("%d.%m.%Y %H:%M"), "photo": png_to_json(return_obj.photo), "name": return_obj.name,
                          "color": return_obj.color, "size": return_obj.size, "quantity": return_obj.quantity,
                          "sale_sum": return_obj.sale_sum, "employer": return_obj.employer} for return_obj in returns]
    except:
        item['sales'] = []


    return item


class GetAllInfoView(APIView):
    def get(self, request):
        return Response(all_data())


class GetUserInfoView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk))


class GetUserDepartmentsView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['departments'])


class GetUserEmployeesView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['employees'])


class GetUserMarkupsView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['markups'])


class GetUserProductsView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['products'])


class GetUserSalesView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['sales'])


class GetUserReturnsView(APIView):
    def get(self, request, pk):
        return Response(user_data(pk)['returns'])


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
    def post(self, request):
        data_dict = request.data
        if data_dict:
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
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                building = data_dict['building']
                level = data_dict['level']
                line = data_dict['line']
                department = data_dict['department']
            except:
                return Response({"error": "No data received!"})

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
        return Response({"error": "No data received!"})


class AddUserEmployeesView(APIView):
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                name = data_dict['name']
                post = data_dict['post']
                status = int(data_dict['status'])
            except:
                return Response({"error": "No data received!"})

            new_employer = Employer()
            new_employer.user = user.profile
            new_employer.name = name
            new_employer.post = post
            new_employer.status = status
            for i in user.profile.employees.all():
                if i.name == name and i.post == post and i.status == status:
                    return Response({"error": "Such a employer already exists at this vendor"})
            new_employer.save()
            return Response({"status": "successfully"})
        return Response({"error": "No data received!"})


class AddUserMarkupView(APIView):
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                name = data_dict['name']
                price_range_from = data_dict['price_range_from']
                price_range_to = data_dict['price_range_to']
                markup = data_dict['markup']
                markup_method = data_dict['markup_method']
            except:
                return Response({"error": "No data received!"})

            new_markup = Markups()
            new_markup.user = user.profile
            new_markup.name = name
            new_markup.price_range_from = int(price_range_from)
            new_markup.price_range_to = int(price_range_to)
            new_markup.markup = int(markup)
            new_markup.markup_method = markup_method
            for i in user.profile.markups.all():
                if i.name == name and i.price_range_from == price_range_from and i.price_range_to == price_range_to and i.markup == markup and i.markup_method == markup_method:
                    return Response({"error": "Such a markup already exists at this vendor"})
            new_markup.save()
            return Response({"status": "successfully"})
        return Response({"error": "No data received!"})


class AddUserProductView(APIView):
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                uid = data_dict['uid']
                name = data_dict['name']
                quantity = data_dict['quantity']
                description = data_dict['description']
                price_purchasing = data_dict['price_purchasing']
                price_retail = data_dict['price_retail']
                price_wholesale = data_dict['price_wholesale']
                price_agent = data_dict['price_agent']
            except:
                return Response({"error": "No data received!"})

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
                    new_photo.photo.save(photo["file_name"], ContentFile(json_to_bytes(photo['image'])))
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
        return Response({"error": "No data received!"})


class AddUserSaleView(APIView):
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                date_time = data_dict['date_time']
                photo = data_dict['photo']
                name = data_dict['name']
                color = data_dict['color']
                size = data_dict['size']
                quantity = data_dict['quantity']
                price = data_dict['price']
                sale_sum = data_dict['sale_sum']
                employer = data_dict['employer']
            except:
                return Response({"error": "No data received!"})

            new_sale = Sales()
            new_sale.user = user.profile
            new_sale.date_time = datetime.datetime.strptime(date_time, "%d.%m.%Y %H:%M")
            new_sale.name = name
            new_sale.color = color
            new_sale.size = size
            new_sale.quantity = quantity
            new_sale.price = price
            new_sale.sale_sum = sale_sum
            new_sale.employer = employer
            for i in user.profile.sales.all():
                if i.name == name and i.color == color and i.size == size and str(i.date_time.strftime("%d.%m.%Y %H:%M")) == str(new_sale.date_time.strftime("%d.%m.%Y %H:%M")):
                    return Response({"error": "Such a sale already exists at this vendor"})
            new_sale.photo.save(photo["file_name"], ContentFile(json_to_bytes(photo['image'])))
            return Response({"status": "successfully"})
        return Response({"error": "No data received!"})


class AddUserReturnView(APIView):
    def post(self, request):
        data_dict = request.data
        if data_dict:
            try:
                user = User.objects.get(id=data_dict['pk'])
            except:
                return Response({'error': "There is no such user"})
            try:
                date_time = data_dict['date_time']
                photo = data_dict['photo']
                name = data_dict['name']
                color = data_dict['color']
                size = data_dict['size']
                quantity = data_dict['quantity']
                price = data_dict['price']
                sale_sum = data_dict['sale_sum']
                employer = data_dict['employer']
            except:
                return Response({"error": "No data received!"})

            new_return = Returns()
            new_return.user = user.profile
            new_return.date_time = datetime.datetime.strptime(date_time, "%d.%m.%Y %H:%M")
            new_return.name = name
            new_return.color = color
            new_return.size = size
            new_return.quantity = quantity
            new_return.price = price
            new_return.sale_sum = sale_sum
            new_return.employer = employer
            for i in user.profile.returns.all():
                if i.name == name and i.color == color and i.size == size and str(i.date_time.strftime("%d.%m.%Y %H:%M")) == str(new_return.date_time.strftime("%d.%m.%Y %H:%M")):
                    return Response({"error": "Such a return already exists at this vendor"})
            new_return.photo.save(photo["file_name"], ContentFile(json_to_bytes(photo['image'])))
            return Response({"status": "successfully"})
        return Response({"error": "No data received!"})


class DeleteUserView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                user.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserDepartmentsView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.departments.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserDepartmentView(APIView):
    def delete(self, request, *args, **kwargs):
        id = request.data['department_id']
        if id:
            try:
                department = Department.objects.get(id=id)
                department.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such department or inlavid data"})
        return Response({"error": "No data received!"})


class DeleteUserEmployeesView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.employees.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserEmployerView(APIView):
    def delete(self, request, *args, **kwargs):
        id = request.data['employer_id']
        if id:
            try:
                employer = Employer.objects.get(id=id)
                employer.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user or inlavid data"})
        return Response({"error": "No data received!"})


class DeleteUserMarkupsView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.markups.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserMarkupView(APIView):
    def delete(self, request, *args, **kwargs):
        id = request.data['markup_id']
        if id:
            try:
                markup = Markups.objects.get(id=id)
                markup.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user or inlavid data"})
        return Response({"error": "No data received!"})


class DeleteUserProductsView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.products.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserProductView(APIView):
    def delete(self, request, *args, **kwargs):
        uid = request.data['uid']
        if uid:
            try:
                product = Products.objects.get(uid=uid)
                product.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user or inlavid data"})
        return Response({"error": "No data received!"})


class DeleteUserSalesView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.sales.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserSaleView(APIView):
    def delete(self, request, *args, **kwargs):
        id = request.data['sale_id']
        if id:
            try:
                sale = Sales.objects.get(id=id)
                sale.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user or inlavid data"})
        return Response({"error": "No data received!"})


class DeleteUserReturnsView(APIView):
    def delete(self, request, *args, **kwargs):
        pk = request.data['pk']
        if pk:
            try:
                user = User.objects.get(id=pk)
                for i in user.profile.returns.all():
                    i.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class DeleteUserReturnView(APIView):
    def delete(self, request, *args, **kwargs):
        id = request.data['return_id']
        if id:
            try:
                return_obj = Returns.objects.get(id=id)
                return_obj.delete()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user or inlavid data"})
        return Response({"error": "No data received!"})


class UpdateUserView(APIView):
    def put(self, request, *args, **kwargs):
        pk = request.data['pk']
        data = request.data['data']
        if pk and data:
            try:
                user = User.objects.get(id=pk)
                if data['password']:
                    user.set_password(data['password'])
                if data['name']:
                    user.profile.name = data['name']
                if data['balance']:
                    user.profile.balance = data['balance']
                if data['status']:
                    user.profile.status = data['status']
                user.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateDepartmentView(APIView):
    def put(self, request, *args, **kwargs):
        id = request.data['department_id']
        data = request.data['data']
        if id and data:
            try:
                department = Department.objects.get(id=id)
                if data['building']:
                    department.building = data['building']
                if data['level']:
                    department.level = data['level']
                if data['line']:
                    department.line = data['line']
                if data['department']:
                    department.department = data['department']
                department.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateEmployerView(APIView):
    def put(self, request, *args, **kwargs):
        id = request.data['employer_id']
        data = request.data['data']
        if id and data:
            try:
                employer = Employer.objects.get(id=id)
                if data['name']:
                    employer.name = data['name']
                if data['post']:
                    employer.post = data['post']
                if data['status']:
                    employer.status = data['status']
                employer.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateMarkupView(APIView):
    def put(self, request, *args, **kwargs):
        id = request.data['markup_id']
        data = request.data['data']
        if id and data:
            try:
                markup = Markups.objects.get(id=id)
                if data['name']:
                    markup.name = data['name']
                if data['price_range_from']:
                    markup.price_range_from = data['price_range_from']
                if data['price_range_to']:
                    markup.price_range_to = data['price_range_to']
                if data['markup']:
                    markup.markup = data['markup']
                if data['markup_method']:
                    markup.markup_method = data['markup_method']
                markup.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateProductView(APIView):
    def put(self, request, *args, **kwargs):
        uid = request.data['uid']
        data = request.data['data']
        if uid and data:
            try:
                product = Products.objects.get(uid=uid)
                if data['name']:
                    product.name = data['name']
                if data['quantity']:
                    product.quantity = data['quantity']
                if data['description']:
                    product.description = data['description']
                if data['price_purchasing']:
                    product.price_purchasing = data['price_purchasing']
                if data['price_retail']:
                    product.price_retail = data['price_retail']
                if data['price_wholesale']:
                    product.price_wholesale = data['price_wholesale']
                if data['price_agent']:
                    product.price_agent = data['price_agent']
                if data['options']:
                    for option in product.options.all():
                        option.delete()
                    for option in data['options']:
                        try:
                            new_option = Options()
                            new_option.product = product
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
                if data['photos']:
                    for photo in product.photos.all():
                        photo.delete()
                    for photo in data['photos']:
                        try:
                            new_photo = Photos()
                            new_photo.product = product
                            new_photo.photo.save(photo["file_name"], ContentFile(json_to_bytes(photo['image'])))
                            new_photo.save()
                        except:
                            pass
                product.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateSaleView(APIView):
    def put(self, request, *args, **kwargs):
        id = request.data['sale_id']
        data = request.data['data']
        if id and data:
            try:
                sale = Sales.objects.get(id=id)
                if data['date_time']:
                    sale.date_time = datetime.datetime.strptime(data['date_time'], "%d.%m.%Y %H:%M")
                if data['name']:
                    sale.name = data['name']
                if data['color']:
                    sale.color = data['color']
                if data['size']:
                    sale.size = data['size']
                if data['quantity']:
                    sale.quantity = data['quantity']
                if data['price']:
                    sale.price = data['price']
                if data['sale_sum']:
                    sale.sale_sum = data['sale_sum']
                if data['employer']:
                    sale.employer = data['employer']
                if data['photo']:
                    sale.photo.save(data["photo"]["file_name"], ContentFile(json_to_bytes(data["photo"]["image"])))
                else:
                    sale.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})


class UpdateReturnView(APIView):
    def put(self, request, *args, **kwargs):
        id = request.data['return_id']
        data = request.data['data']
        if id and data:
            try:
                return_obj = Returns.objects.get(id=id)
                if data['date_time']:
                    return_obj.date_time = datetime.datetime.strptime(data['date_time'], "%d.%m.%Y %H:%M")
                if data['name']:
                    return_obj.name = data['name']
                if data['color']:
                    return_obj.color = data['color']
                if data['size']:
                    return_obj.size = data['size']
                if data['quantity']:
                    return_obj.quantity = data['quantity']
                if data['price']:
                    return_obj.price = data['price']
                if data['sale_sum']:
                    return_obj.sale_sum = data['sale_sum']
                if data['employer']:
                    return_obj.employer = data['employer']
                if data['photo']:
                    return_obj.photo.save(data["photo"]["file_name"], ContentFile(json_to_bytes(data["photo"]["image"])))
                else:
                    return_obj.save()
                return Response({"status": "successfully"})
            except:
                return Response({'error': "There is no such user"})
        return Response({"error": "No data received!"})