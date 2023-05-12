from rest_framework import serializers
from .models import Product, Users, Promotion


class MenuSerializer (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['Name','Title','Description','Price','AvaliableDate', 'StockQuantity', 'Image_1', 'Image_2', 'Image_3' ];
        
class UsersSerializer (serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['UserName','SiteID' ];
        
class PromotionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['Promotion_Id','Product_Id', 'User' ];
        
        