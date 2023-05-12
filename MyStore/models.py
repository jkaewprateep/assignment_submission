from django.db import models
from django.contrib.auth.models import User;

### ADD ###
from datetime import datetime;
from django.core.exceptions import ValidationError;


# ### ADD
# def create_user(self, email, password=None):
#     """
#     Creates and saves a User with the given email and password.
#     """
#     if not email:
#         raise ValueError('Users must have an email address')

#     user = self.model(
#     email=self.normalize_email(email),
#     )

#     user.set_password(password)
#     user.save(using=self._db)
#     return user
# ###

# Create your models here.
# class Category( models.Model ):
#     slug = models.SlugField();
#     Title = models.CharField(max_length=255);
    
#     def __str__(self)-> str:
#         return self.Title

class Users( models.Model ):
    def validate_user( value ):
          
        if len(User.objects.filter(username=value).values()) < 1 :
            raise ValidationError( str( value ) + " " + str("is not members of user") );
        
    UserName = models.CharField(max_length=255, validators=[validate_user]);
    SiteID = models.SmallIntegerField(default=0);


class Promotion( models.Model ):
    def validate_user( value ):
          
        if len(User.objects.filter(username=value).values()) < 1 :
            raise ValidationError( str( value ) + " " + str("is not members of user") );
        
    Promotion_Id = models.SmallIntegerField(default=0);
    Product_Id = models.SmallIntegerField(default=0);
    User = models.CharField(max_length=255, validators=[validate_user]);

# class Promotion( models.Model ):
    
#     def validate_user( value ):
          
#         if len(User.objects.filter(username=value).values()) < 1 :
#             raise ValidationError( str( value ) + " " + str("is not members of user") );
        
#     Promotion_Id = models.SmallIntegerField(default=0);
#     Product_Id = models.SmallIntegerField(default=0);
#     User = models.CharField(max_length=255, validators=[validate_user]);
    
# a title, description, price, available date, stock quantity, and product images
class Product( models.Model ):

    Product_Id = models.SmallIntegerField(default=0);
    Name = models.CharField(max_length=255);
    Title = models.CharField(max_length=255);
    Description = models.CharField(max_length=255);
    Price = models.DecimalField(max_digits=10, decimal_places=2);
    # AvaliableDate = models.DateField(default=datetime.now());
    AvaliableDate = models.DateField();
    StockQuantity = models.DecimalField(max_digits=10, decimal_places=0);
    Image_1 = models.CharField(max_length=512);
    Image_2 = models.CharField(max_length=512);
    Image_3 = models.CharField(max_length=512);
    Promotion_Id = models.ForeignKey(Promotion, on_delete=models.PROTECT, default=1) 

    def __str__(self): 
        return self.Name
    


    
    
# class User( models.Model ):
#     Title = models.CharField(max_length=255);
#     Name = models.CharField(max_length=255);
#     Promotion_product = models.ForeignKey(Product, on_delete=models.PROTECT, default=1) 
    
#     def __str__(self): 
#         return self.Name
    
# Add code to create Menu model
# class Menu(models.Model):
#     MeunTitle = models.CharField(max_length=255);
#     Title = Product.Title;
#     Price = Product.Price;
#     StockQuantity = Product.StockQuantity;
#     category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1) 

#     def __str__(self):
#         return self.Title;