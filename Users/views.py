# django libraries
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
# from django.forms.models import model_to_dict
# simple libraries
import random
# local importing
from .models import *
from .serializer import *
# from decimal import Decimal
# Create your views here.
#! NAMING

otp_generation = random.randint(1111, 9999)


class Register_view_step1(APIView):
    queryset = Users.objects.all()
    serializer = Phone_Reg_srl()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Phone_Reg_srl)
    def post(self, request):

        request.data['otp'] = str(otp_generation)
        serializer = Otp_Reg_srl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"MSG": "Successfully created", "OTP": otp_generation})
        else:
            return Response(serializer.errors)


class Register_step2(APIView):
    queryset = Users.objects.all()
    serializer = Otp_Reg_srl()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Otp_Reg_srl)
    def post(self, request):
        re_phone = request.data.get("phone")
        re_password = request.data.get("otp")
        check = Users.objects.filter(otp=re_password, phone=re_phone).first()
        if check:
            return Response({"MSG": "Succsesfuly"})
        else:
            return Response(status=400)


class Main_Reg(APIView):
    queryset = Users.objects.all()
    serializer = User_Srl()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=User_Srl)
    def post(self, request):
        phone = request.data.get("phone")
        name = request.data.get("name")
        surname = request.data.get("surname")
        password = request.data.get("password")

        user = Users.objects.get(phone=phone)
        if user:
            user.name = name
            user.surname = surname
            user.password = make_password(password)
            user.save()

            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "data": User_Srl(user).data
            })
        else:
            return Response({"MSG": "ERROR"}, status=400)

        # user = Users.objects.filter(phone=phone).update(
        #     name=name, surname=surname, password=password)
        # print(user)
        # if user:
        #     access = AccessToken.for_user(user)
        #     refresh = RefreshToken.for_user(user)
        #     return Response({
        #         "access": access,
        #         "refresh": refresh,
        #         "data": user
        #     })
        # else:
        #     return Response({"MSG": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    queryset = Users.objects.all()
    serializer = Log_user()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Log_user)
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        log_user = Users.objects.filter(phone=phone).first()
        print(log_user)
        if log_user and check_password(password, log_user.password):
            print("if kirdi")
            access = AccessToken.for_user(log_user)
            refresh = RefreshToken.for_user(log_user)
            serializer = Log_user(log_user)
            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "serializer": serializer.data
            })
        else:
            return Response({"MSG": "ERROR"}, status=400)


class Change_Password(generics.UpdateAPIView):
    queryset = Users.objects.all()  # You can adjust this queryset as needed
    serializer_class = Change_Srl
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,]

    def update(self, request, pk=None, *args, **kwargs):
        user = self.get_object()

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect."}, status=401)

        if new_password != confirm_password:
            return Response({"error": "New password and confirm password do not match."}, status=400)

        user.password = make_password(str(new_password))
        user.save()

        return Response({"message": "Password updated successfully."}, status=200)


class All_Users(APIView):
    queryset = Users.objects.all()
    serializer = Show_Users_Srl()

    def get(self, request):
        selected = Users.objects.all()
        serializer = Show_Users_Srl(selected, many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Forgot_Password_step1(APIView):
    queryset = Users.objects.all()
    serializer = Phone_Reg_srl()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Phone_Reg_srl)
    def post(self, request):
        phone = request.data.get("phone")
        user = Users.objects.filter(phone=phone).first()
        if user:
            return Response({"OTP": user.otp})
        else:
            return Response({"MSG": "Bunday User yoq"})


class Forgot_Password_step2(APIView):
    queryset = Users.objects.all()
    serializer = Forgot_pass()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Forgot_pass)
    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")
        password = request.data.get("password")
        try:
            user = Users.objects.all().filter(phone=phone, otp=otp).update(password=password)
            return Response({"MSG": "PASSWORD IS CHANGED!"})
        except:
            return Response({"MSG": "ERROR"})


class Delete_User(APIView):
    queryset = Users.objects.all()
    # serializer = Forgot_pass()

    def delete(self, request, pk):
        user = Users.objects.filter(id=pk)
        user.delete()
        return Response({"MSG": "Delete"})


class Select_User(APIView):
    queryset = Users.objects.all()
    serializer = Show_Users_Srl()

    def get(self, request, pk):
        selected = Users.objects.filter(id=pk).first()
        serializer = Show_Users_Srl(selected)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Logout_users(APIView):
    queryset = Users.objects.all()

    def get(self, request, pk):
        user = Users.objects.get(id=pk)
        if user:
            logout(request)
            return Response({"MSG": "Succsess"})
        else:
            return Response({"MSG": "error"})


### Orders ###

class OrderViews(APIView):
    queryset = Orders.objects.all()
    serializer = OrdersSrl
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=OrdersSrl)
    def post(self, request):
        # re_product = request.data.get("product")
        # re_user = request.data.get('user')
        # user = Users.objects.filter(id=re_user).first()
        # product = Product.objects.filter(id=re_product).first()
        serializer = OrdersSrl(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Phone_Changer(APIView):
    queryset = Users.objects.all()
    serializer = Change_SRL
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=Change_SRL)
    def patch(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = Change_SRL(data=request.data)
            if serializer.is_valid():
                change_phone = request.data.get('change_phone')
                if len(change_phone) >= 9 and user.phone != change_phone:
                    user.phone = change_phone
                    user.save()
                    return Response({'MSG': 'Successfully updated phone number'})
                else:
                    return Response({'Error': 'phone is not valid'}, status=404)
            else:
                return Response(serializer.errors)
        except:
            return Response({'Error': 'User not found'}, status=404)


class CardUser(APIView):
    queryset = Users.objects.all()
    serializer = CardUserSrl
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=CardUserSrl)
    def patch(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
        except:
            return Response({'Error': 'User not found'}, status=404)
        user.idp = request.data.get('idp', user.idp)
        user.seria = request.data.get('seria', user.seria)
        user.raqam = request.data.get('raqam', user.raqam)
        user.pasport = request.data.get('pasport', user.pasport)
        user.image = request.data.get('image', user.image)
        user.card = request.data.get('card', user.card)
        user.card_number = request.data.get('card_number', user.card_number)
        user.addres = request.data.get('addres', user.addres)
        user.viloyat = request.data.get('viloyat', user.viloyat)
        user.save()

        return Response({'Success': 'User updated successfully'}, status=200)


class Calculate_cash_order(APIView):
    queryset = Orders.objects.all()
    serializer = OrdersSrl
    serializer = AllProductsSRL

    def get(self, request, pk):
        try:
            order = Orders.objects.filter(id=pk).first()
        except:
            return Response({"MSG": "Order not found"}, status=404)

        if order:
            if order.payment == 'cash':
                product = Product.objects.filter(id=order.product.id).first()
                cost = int(product.cost)*int(order.quantity)
                order_srl = OrdersSrl(order)
                product_srl = AllProductsSRL(product)
                if order.quantity <= product.quantity:
                    return Response(
                        {
                            "ORDER": order_srl.data,
                            "PRODUCT": product_srl.data,
                            "TOTAL": cost,
                        }
                    )  # {'product_id': product_id, 'name': product.name, 'cost': cost}
                else:
                    return Response({"MSG": "Quantity not available"})
            elif order.payment == 'credit':
                product = Product.objects.filter(id=order.product.id).first()
                credit_cost = int(product.cost)*int(order.quantity)
                if order.quantity <= product.quantity:
                    total_cost = credit_cost * \
                        (pow((1+int(order.product.protsent)),
                         int(order.period)))/int(order.period)  # ! creditformula 1+protsent**period=cost/period=credit
                    return Response(
                        {
                            "name": product.name,
                            "TOTAL COST P/MONTH": str(total_cost),
                        }
                    )

                else:
                    return Response({"MSG": "Quantity not available"})
            else:
                return Response({"MSG": "bunday tolov turi mavjud emas"})
        else:
            return Response({"MSG": "Not found this order"})


class Users_Order_all_views(APIView):
    queryset = Users.objects.all()

    def get(self, request, pk):
        try:
            # filter
            user = Users.objects.get(id=pk)
            orders = Orders.objects.all().filter(user=user.id)
            product_ids = [i.product.id for i in orders]
            print(product_ids)
            products_list = []
            for i in range(len(product_ids)):
                products = Product.objects.all().filter(id=product_ids[i])
                products_list.extend(products)

            serializer = AllProductsSRL(products_list, many=True)
            return Response(
                {
                    "USER": {'id': user.id, "name": user.name},
                    "PRODUCTS": serializer.data,
                }
            )
        except:
            return Response({'Error': 'User not found'}, status=404)


class User_order_all_delete(APIView):
    queryset1 = Users.objects.all()
    queryset2 = Orders.objects.all()
    parser_classes = [MultiPartParser,]

    @swagger_auto_schema(request_body=DeleteOrderSrl)
    def delete(self, request, pk):
        re_id = request.data.get("id")
        try:
            user = Users.objects.get(id=pk)
        except Users.DoesNotExist:
            return Response('User not found', status=404)
        orders = Orders.objects.all().filter(user=user)
        if orders.filter(product_id=re_id).exists():
            orders.filter(product_id=re_id).delete
            return Response("Delete successful")
        else:
            return Response('Order not found', status=404)


class PaymentSystemViews(APIView):
    queryset = Users.objects.all()
    serializer = CardUserSrl
    parser_classes = [MultiPartParser,]

    def post(self, request, pk):
        pass
# card + bosilganda is_buy true boladi va korzinkaga tushadi qachon tolov bogandan keyin status buyurtma qabul qilindiga aylanadi viloyat bizaga uzoroda bosa kun kopro berilishi mumkun
