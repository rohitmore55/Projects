from django.contrib import admin
from cstoreapp.models import product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','details','Price','catagory','availability']
    list_filter=['Price','catagory','availability']

admin.site.register(product,ProductAdmin)
