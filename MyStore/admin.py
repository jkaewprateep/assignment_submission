from django.contrib import admin

# Register your models here.
from .models import Product, Promotion, Users

admin.site.register( Promotion );
admin.site.register( Product );
admin.site.register( Users );