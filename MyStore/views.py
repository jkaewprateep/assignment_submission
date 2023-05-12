from django.shortcuts import render

# Create your views here.
from datetime import datetime
from .models import Product, Promotion, Users
from django.contrib.auth.models import User
from .serializers import MenuSerializer, UsersSerializer, PromotionSerializer
from django.http import HttpResponse
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response;
from rest_framework.decorators import api_view, permission_classes;
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import generics;
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms

from rest_framework.authtoken.models import Token
import json
import jwt
import base64

# class AvaliableDateStart_Form(forms.Form):
#     AvaliableDateStart_text = forms.CharField(label="AvaliableDateStart", max_length=100)
    
# class AvaliableDateEnd_Form(forms.Form):
#     AvaliableDateEnd_text = forms.CharField(label="AvaliableDateEnd", max_length=100)
    
    # AvaliableDateEnd_text = forms.CharField(label="AvaliableDateEnd", max_length=100)
    # Promotion_search_text = forms.CharField(label="Promotion_search", max_length=100)
    # avaliable_only_text = forms.BooleanField(label="avaliable_only")
    # newset_on_top_text = forms.BooleanField(label="newset_on_top")
    

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html')

def loginpage(request):
    return render(request, 'login.html')

def menu(request):

    request.session['username'] = 'jirayukaewprateep'

    data = request.POST
    
    AvaliableDateStart = ""
    AvaliableDateEnd = ""
    Promotion_search = ""
    avaliable_only = ""
    newset_on_top = ""
    userSiteID = ""
    ls_Promotion_Id = []
    ls_Product_Id = []
    username_filed = request.session.get('username')
    
    # request.session['username'] = 'jirayukaewprateep'
    
    # if len([ x for x in data if x == "custom" ]) > 0 :
    #     print( 'data[custom]' )
    #     print( data['custom'] )
    
    if len([ x for x in data if x == "AvaliableDateStart" ]) > 0 :
        AvaliableDateStart = data['AvaliableDateStart']
    if len([ x for x in data if x == "AvaliableDateEnd" ]) > 0 :
        AvaliableDateEnd = data['AvaliableDateEnd']
    if len([ x for x in data if x == "Promotion_search" ]) > 0 :
        Promotion_search = data['Promotion_search']
    if len([ x for x in data if x == "avaliable_only" ]) > 0 :
        avaliable_only= data['avaliable_only']
    if len([ x for x in data if x == "newset_on_top" ]) > 0 :    
        newset_on_top = data['newset_on_top']
    # if len([ x for x in data if x == "username" ]) > 0 :
    #     username_filed = data['username']
        # request.session.setdefault('username', username_filed)
        
    # print( request.session.get('username') )
    # request.session.set('username', 'jirayukaewprateep')
        
        # request.session['username'] = 'jirayukaewprateep'
        # request.session['person'] = {'name': 'John', 'age': 27}
    
    print( AvaliableDateStart )
    print( AvaliableDateEnd )
    print( Promotion_search )
    print( avaliable_only )
    print( newset_on_top )
    print( username_filed )
    
    menu_data = Product.objects.all()
    
    
    
    if len( username_filed ) > 0 :
        print('condition 1: username only')
        user_data = Users.objects.filter(UserName=username_filed)
        userSiteID = user_data.values_list()[0][2]


        menu_data = menu_data
        if userSiteID == "1" :
            menu_data = menu_data.objects.all()
        else :
            promotion_data = Promotion.objects.filter(User=username_filed)
            
            for item in promotion_data.values():
                ls_Promotion_Id.append(item['Promotion_Id']); 
                ls_Product_Id.append(item['Product_Id']); 
            
            
            menu_data = menu_data.filter(Promotion_Id__in=ls_Promotion_Id)
            print( menu_data )
            # [startdate, enddate]
            
    else:
        main_data = {"menu": []}
        return render(request, 'menu.html', {"menu": main_data})
    
    if len( AvaliableDateStart ) > 0 and len( AvaliableDateEnd ) > 0 :
        print('condition 2: avaliable date')
        menu_data = menu_data.filter(AvaliableDate__range=[ AvaliableDateStart, AvaliableDateEnd ])
        
        print( menu_data )
        
    if len( Promotion_search ) > 0  :
        print('condition 3: promotion search')
        if Promotion_search != "Monster Randoms" :
            menu_data = menu_data.filter(Promotion_Id__in=ls_Promotion_Id)
            
        print( menu_data )
    
    if len( avaliable_only ) > 0 :
        print('condition 4: avaliable only')
        menu_data = menu_data
        
        ls_pk_not_avaliable = []
        ls_items = menu_data.values_list()
        for item in ls_items :
            print( str(item[0]) + " " + str(item[7]) )
            if item[7] < 1 :
                ls_pk_not_avaliable.append(item[0])
                menu_data.get(pk=item[0]).delete()
        
        print( menu_data.values_list() )
        
    if len( newset_on_top ) > 0 :
        print('condition 5: newest on top')
        if newset_on_top == "yes" :
            menu_data = menu_data.order_by('AvaliableDate')
        else :
            menu_data = menu_data.order_by('AvaliableDate')[::-1]
            
        print( menu_data )
    
    

    # menu_data = Product.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


# category, newest/oldest, or availability status (in-stock or out-of-stock) 


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def createuser(request):
    
    input_as_dict = dict(request.data);
    
    ### Count Keys input
    count = 0

    for key,value in input_as_dict.items():
        count += 1
    ###
    
    if count > 0 :

        email = input_as_dict['email']
        password = input_as_dict['password']
        username = input_as_dict['username']
    
        user = User.objects.create_user(username, email, password)

        # At this point, user is a User object that has already been saved
        # to the database. You can continue to change its attributes
        # if you want to change other fields.
        # user.last_name = "Lennon"
        user.save()
        
    else:
        return HttpResponse(str("{'User Not exists'}"));

@api_view(['POST'])
def signin(request):
    
    input_as_dict = dict(request.data);

    ### Count Keys input
    count = 0

    for key,value in input_as_dict.items():
        count += 1
    ###
    
    if count > 0 :

        email = input_as_dict['email']
        password = input_as_dict['password']
        username = ""
        
        ## True / False for existing filtered
        if  User.objects.filter(email=email).exists():
        
            user = authenticate(request, username=username, password=password)
            
            print( User.objects.all() )
            # <QuerySet [<User: admin>, <User: Adrian>, <User: Mario>, <User: Sana>, <User: Registration_Name>, <User: New_customer_01>, 
            # <User: New_customer_02>]>
            
            temp = User.objects.filter(email=email).values();
            print( 'temp.values()' )
            print( Token.objects.get_or_create(user= User.objects.filter(email=email).first() ) )
            token, created = Token.objects.get_or_create(user= User.objects.filter(email=email).first())
        
            return HttpResponse("{ \"token\"" + ": " + "\"" + str(token) + "\" }");
    
        else:
                return HttpResponse(str("{'User Not exists'}"));
            
    else : 
    
        string_response = ""
        string_response = string_response +  "No valid inputs please use this format" + "{ "
        string_response = string_response +"\"email\"" + ": " + "\"mario@littlelemon.com\","
        string_response = string_response +"\"password\"" + ": " + "\"1234\","
        string_response = string_response +" }"
        string_response = str(string_response);
    
    
    return HttpResponse(string_response);
        

# @api_view(['GET', 'POST'])
# def assignusersiteID(request):
    
#     input_as_dict = dict(request.data);

#     ### Count Keys input
#     count = 0

#     for key,value in input_as_dict.items():
#         count += 1
#     ###
    
#     if count > 0 :

#         UserName = input_as_dict['UserName']
#         SiteID = input_as_dict['SiteID']
        
#         exist = Users.objects.filter(UserName=UserName).exists()
        
#         if exist==False:
            
#             user =- Users(
#                 UserName = UserName,
#                 SiteID = SiteID,
#             )
#             user.save()
#         else:
#             return HttpResponse("{'error':1}", content_type='application/json')
        
#     AllUsers = Users.objects.all();
#     AllUsers_json = serializers.serialize('json', AllUsers)

#     return HttpResponse(AllUsers_json, content_type='application/json')


class assignusersiteIDView(generics.CreateAPIView):
    
    model = Users
    fields = ['UserName','SiteID' ];
    success_url = reverse_lazy('tasks');
    serializer_class = UsersSerializer;
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        return super(assignusersiteIDView, self).form_valid(form)
    
    # def list(self, request):
        
    #     data = request.query_params


@csrf_exempt
def products(request):
    
    if request.method == 'POST':
        data = json.load(request)
        
        exist = Product.objects.filter(Name=data['Name']).exists()
        
        # exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
        #     reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            product = Product(
                Name=data['Name'],
                Title=data['Title'],
                Description=data['Description'],
                Price=data['Price'],
                AvaliableDate=data['AvaliableDate'],
                StockQuantity=data['StockQuantity'],
                Image_1=data['Image_1'],
                Image_2=data['Image_2'],
                Image_3=data['Image_3'],
                
            )
            product.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Product.objects.all().filter(AvaliableDate=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')


@csrf_exempt
def promotions(request):
    
    if request.method == 'POST':
        data = json.load(request)
        
        exist = Promotion.objects.filter(Promotion_Id=data['Promotion_Id']).exists()
        
        # exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
        #     reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            
            promotion = Promotion(
                
                Promotion_Id = data['Promotion_Id'],
                Product_Id = data['Product_Id'],
                User = data['User'],
            )
            

            promotion.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Promotion.objects.all()
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

class promotions_as_view(generics.ListCreateAPIView):
    model = Promotion
    queryset = Promotion.objects.all();
    serializer_class = PromotionSerializer;
    ordering_fields = ['Promotion_Id','Product_Id', 'User' ];
    filterset_fields = ['Promotion_Id','Product_Id', 'User' ];
    search_fields = ['Promotion_Id','Product_Id', 'User' ];

class MenuView(generics.ListCreateAPIView):
    
    queryset = Product.objects.all();
    serializer_class = MenuSerializer;
    ordering_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    filterset_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    search_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    
    def list(self, request):
        
        data = request.query_params
        
        
        if len([ x for x in request.headers if x == "Authorization" ]) > 0 :
       
            # base64_message = 'UHl0aG9uIGlzIGZ1bg=='
            base64_bytes = request.headers['Authorization'].replace('Basic ', '').encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            username = message.split(':')
            username = username[0]
            password = username[1]
            print( username )
            
            ls_permission_productID = []
            ls_usersiteID = []
            Is_userStoreFront = False
            
            if len(username) > 0 :
                queryset = Promotion.objects.all().filter(User=username);
                for item in queryset.values():
                    ls_permission_productID.append(item['Product_Id']);
                
                usersiteID = Users.objects.all().filter(UserName=username);
                for item in usersiteID.values():
                    ls_usersiteID.append(item['SiteID']);
                    
                    if item['SiteID'] == 1 :
                        Is_userStoreFront = True;
                        break;

            if ( Is_userStoreFront ):
                
                if len([ x for x in list(data.keys()) if x == "Name" ]) > 0 :
                    if len([ x for x in list(data.keys()) if x == "AvaliableDate" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Name']).filter(Name=data['AvaliableDate'])
                    elif len([ x for x in list(data.keys()) if x == "Price" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Name']).filter(Name=data['Price'])
                    elif len([ x for x in list(data.keys()) if x == "Title" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Title']).filter(Name=data['Name'])
                    else:
                        queryset = self.get_queryset().filter(Name=data['Name'])
                    serializer = MenuSerializer(queryset, many=True)
                    
                else :
                            
                    serializer = MenuSerializer(self.get_queryset(), many=True)
                return Response(serializer.data)
                
            else:

                if len([ x for x in list(data.keys()) if x == "Name" ]) > 0 :
                    if len([ x for x in list(data.keys()) if x == "AvaliableDate" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Name']).filter(Name=data['AvaliableDate']).filter(Promotion_Id__in=ls_permission_productID)
                    elif len([ x for x in list(data.keys()) if x == "Price" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Name']).filter(Name=data['Price']).filter(Promotion_Id__in=ls_permission_productID)
                    elif len([ x for x in list(data.keys()) if x == "Title" ]) > 0 :
                        queryset = self.get_queryset().filter(Title=data['Title']).filter(Name=data['Name']).filter(Promotion_Id__in=ls_permission_productID)
                    else:
                        queryset = self.get_queryset().filter(Name=data['Name']).filter(Promotion_Id__in=ls_permission_productID)
                    serializer = MenuSerializer(queryset, many=True)
                    
                else :
                            
                    serializer = MenuSerializer(self.get_queryset(), many=True)
                return Response(serializer.data)
        
        else:
            
            
            data
            
            return HttpResponse("{'error': No username provided }", content_type='application/json')
        
class MenuView_as_view(generics.ListCreateAPIView):
    model = Product
    queryset = Product.objects.all();
    serializer_class = MenuSerializer;
    ordering_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    filterset_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    search_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];

class MenuView_readupdate_as_view(generics.RetrieveUpdateAPIView):
    model = Product
    queryset = Product.objects.all();
    serializer_class = MenuSerializer;
    lookup_field = 'Name'
    ordering_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    filterset_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    search_fields = ['Name', 'Title' ,'Description', 'Price', 'AvaliableDate', 'StockQuantity'];
    
# class MenuView_readupdate_as_view(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAdminUser)
#     serializer_class = MenuSerializer
#     lookup_field = 'username'

#     def get_object(self):
#         username = self.kwargs["username"]
#         return get_object_or_404(User, username=username)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)


class MenuView_readupdate_as_view(generics.ListAPIView):

    model = Product
    serializer_class = MenuSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Name', 'Price']
    