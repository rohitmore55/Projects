from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=20,verbose_name="Product_Name")
    details=models.CharField(max_length=50,verbose_name="Product_Details")
    Price=models.FloatField()
    cat=((1,"Shirts"),(2,"T-shirts"),(3,"Jeans"),(4,"Joggers"),(5,"Undergarments"))
    catagory=models.IntegerField(choices=cat)
    availability=models.BooleanField(default=True,verbose_name="Product Active/Inactive")
    pimage=models.ImageField(upload_to='image')

class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)

class order(models.Model):
    orderid=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(product,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)



    



